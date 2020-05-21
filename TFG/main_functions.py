import numpy as np
import json
from jsonschema import *
import requests
import os
import sys
import time

#Se define el constructor del tipo Active, con los campos que posee cada activo de red
class Active:
    def __init__(self, ip,services,software,os,ja3,useragents):
        self.ip=ip
        self.services=services
        self.software=software
        self.os=os
        self.ja3=ja3
        self.useragents=useragents

# JSON Schema de un activo de red
schema = {
    "type" : "object",
    "properties":{
        "IP": {"type" : "string"},
        "OS": {"type":["string","array"]},
        "Services":{"type":["string","array"]},
        "Software":{"type":["string","array"]},
        "JA3_Fingerprint":{"type":["string","array"]},
        "Possible User-Agent":{"type":["string","array"]}
    },
    "required": ["IP"]
}
# Funcion para validar el JSON Schema e incluirlo en una lista
def validate_and_add(item,schema,list):
  validate(item, schema=schema)
  list.append(item)

# Funcion para quedarse con los elementos unicos de una lista
def unique(list1):
    # Inserta la lista en el set
    list_set = set(list1)
    # Convierte el set en una lista de nuevo
    unique_list = (list(list_set))
    final_list=[]
    for x in unique_list:
        final_list.append(str(np.unique(x))[1:-1].replace("'", ""))
    return final_list

# Funcion para eliminar caracteres sobrantes repetidos
def cleanname(name):
    name = str(name).replace('""', '')
    name = str(name).replace('""', '')
    name = str(name).replace('"', '')
    name = str(name).replace("#", '')
    name = str(name).replace(";", '')
    return name

# Funcion para leer el archivo conn.log y extraer las direcciones IP
def readips(rutatolog):
    reader=open(rutatolog, 'r')
    listahosts = []
    for line in reader:
        jsonreader = json.loads(line)
        listahosts.append(jsonreader['id.orig_h'])
        listahosts.append(jsonreader['id.resp_h'])
    listaips=unique(listahosts)
    return listaips

# Funcion para leer el archivo JA3er.json y guardar un diccionario de md5:User-Agent 
def readja3(rutatolog):
    d=dict()
    data = json.load(open(rutatolog, 'r'))
    for user in data:
        d[user['md5']]=user['User-Agent'] 
    return d

# Funcion para extraer los servicios de red encontrados en el fichero de known services
def knownservices(ips,actives,rutatolog):
    # Leemos el json de los known_services
    reader = open(rutatolog, 'r')
    lines=[]
    for line in reader:
        row = json.loads(line)
        lines.append(row)

    # Para cada una de las lineas, se busca si coincide la IP y se registran los servicios
    for line in lines:
        actives[ips.index(line['host'])].services.append(line['service'][0])
    return actives

# Funcion para extraer los software encontrados en el fichero software
def software(ips,actives,rutatolog):
    reader = open(rutatolog, 'r')
    lines = []
    for line in reader:
        row = json.loads(line)
        lines.append(row)

    for row in lines:
        name=row['unparsed_version']
        name=cleanname(name)
        # Detectar algun SO gracias al software
        if ("ubuntu" in str(np.unique(str(row['unparsed_version']))))or ("Ubuntu" in str(np.unique(str(row['unparsed_version'])))) or ("Debian" in str(np.unique(str(row['unparsed_version'])))):
            actives[ips.index(row['host'])].os.append("Linux")
        elif ("Windows" in str(np.unique(str(row['unparsed_version'])))):
            actives[ips.index(row['host'])].os.append("Windows")
        if (len(name) < 100): # De nuevo para eliminar longitud excesiva
            actives[ips.index(row['host'])].software.append(name)

     
    return actives

# Funcion para extraer los hashes JA3 y JA3S de clientes y servidores SSL
def ja3reader(ips,actives,rutatolog):
    reader = open(rutatolog, 'r')
    lines=[]
    for line in reader:
        row = json.loads(line)
        lines.append(row)

    # Para cada una de las lineas, se busca si coincide la IP y se registran los hashes JA3 y JA3S
    
    for row in lines:
        if row['established']==True:
            actives[ips.index(row['id.orig_h'])].ja3.append(row['ja3'])
            actives[ips.index(row['id.resp_h'])].ja3.append(row['ja3s'])
    return actives

# Funcion para extraer del fichero de p0f los Sistemas Operativos
def p0freader(ips,actives,rutatolog):
    with open(rutatolog) as reader:
        finallist=[]
        for line in reader:
            fields = line.split('|')
            if fields[3] =='subj=cli':
                os = []
                ip=fields[1].split('=')[1].split('/')[0]
            
                if 'os' in fields[4]:

                    if '???' in fields[4]:
                        os=[]
                    else:
                        actives[ips.index(ip)].os.append(fields[4].split('=')[1])
            if fields[3] == 'subj=srv':
                os = []
                ip = fields[2].split('=')[1].split('/')[0]
                if 'os' in fields[4]:
                    if '???' in fields[4]:
                        os = []

                    else:
                        actives[ips.index(ip)].os.append(fields[4].split('=')[1])
    return actives

# Funcion para realizar busqueda en la bbdd de ja3er y recuperar los User-Agents
def ja3lookup(ja3fing,d):
    useragents=[]
    for user in ja3fing:
        if(user in d.keys()):
            useragents.append(d[user])
    return useragents

# Funcion para escribir data.json
def writedata(rutatolog,data):
    writer=open(rutatolog+"data.json", 'w')
    nlines=0
    currentline=0
    for line in data:
        nlines=nlines+1

    writer.write("[")
    for line in data:
        line=str(line).replace("'", '"')
        line=str(line).replace("#", '')
        writer.write(line)
        if(currentline!=nlines-1):
            writer.write(",")
        currentline=currentline+1
    writer.write("]")

cwd=os.getcwd()
os.system("figlet Active-mapper")
print("Introduce the base directory where the pcap is located: ")
dir=sys.stdin.readline().strip()
print("Do you want to create the graph associated to the pcap? [y/n] (default n)")
decision=sys.stdin.readline().strip()
start_time = time.time()
os.system("export PATH=/opt/zeek/bin:$PATH && cd "+dir+" && zeek -Cr "+dir+"*.pcap local")
os.system("p0f -r "+dir+"*.pcap -o "+dir+"p0f.log > /dev/null")

d=readja3(cwd+"/JA3db.json");
listaips=readips(dir+'conn.log')
listaactivos=[]
for ip in listaips:    #Se crean todos los activos vacios con solo la IP
    activo = Active(ip,[],[],[],[],[])
    listaactivos.append(activo)	

listaactivos=knownservices(listaips,listaactivos,dir+'known_services.log')
listaactivos=software(listaips,listaactivos,dir+'software.log')
listaactivos=ja3reader(listaips,listaactivos,dir+'ssl.log')
listaactivos=p0freader(listaips,listaactivos,dir+'p0f.log')
print("Finished reading files in %s seconds" % (time.time() - start_time))
start_time = time.time()
for activo in listaactivos:
    users=[]
    activo.ja3 = unique(activo.ja3)
    activo.useragents=ja3lookup(activo.ja3,d)
print("Finished the ja3 lookup in %s seconds" % (time.time() - start_time))
 
start_time = time.time()
for activo in listaactivos:
    activo.os=unique(activo.os)
    activo.services=unique(activo.services)
    activo.software=unique(activo.software)

network=[]
print("Finished getting the unique data in %s seconds" % (time.time() - start_time))
start_time = time.time()

# Formar los activos y agregarlos a la CMDB en data.json
for activo in listaactivos:
    active={
        "IP":activo.ip,
        "OS":activo.os,
        "Services":activo.services,
        "Software":activo.software,
        "JA3_Fingeprint":activo.ja3,
        "Possible User-Agent":activo.useragents
    }
    if activo.ip not in ['255.255.255.255','0.0.0.0','::']:
        validate_and_add(active,schema,network)
print("Finished validating the JSON in %s segundos" % (time.time() - start_time))

writedata(dir,network)
os.system("cat "+dir+"data.json > "+cwd+"/templates/data.json")
if(decision =='y'):
    start_time = time.time()
    # Uso de brassfork y CSVtoGEXF para obtener el grafo de GEPHI en out.gexf
    tmp = os.popen("ls "+dir+"*.pcap").read()
    command ="./brassfork -nodes="+dir+"nodes.csv -edges="+dir+"edges.csv"+" -in="+tmp
    os.system("cd "+cwd+"&& "+command)
    os.system("sed 's/,/"+"\t"+"/g' "+dir+"nodes.csv"+" > "+dir+"finalnodes.csv")
    os.system("sed 's/,/"+"\t"+"/g' "+dir+"edges.csv"+" > "+dir+"finaledges.csv")
    os.system("tr '[:upper:]' '[:lower:]' <"+dir+"finaledges.csv >"+dir+"outputedges.csv")
    os.system("tr '[:upper:]' '[:lower:]' <"+dir+"finalnodes.csv >"+dir+"outputnodes.csv")
    print("Finished using brassfork in %s seconds" % (time.time() - start_time))

    start_time = time.time()
    os.system("python3 convCSVtoGEXF.py -n "+dir+"outputnodes.csv -e "+dir+"outputedges.csv -d "+cwd+"/definitions.txt")
    os.system("mv "+cwd+"/out.gexf "+dir)
    os.system("rm "+dir+"*.csv")
    print("Finished the GEXF creation in %s seconds" % (time.time() - start_time))
