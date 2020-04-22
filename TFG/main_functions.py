import numpy as np
import json
from jsonschema import *
import requests
import os
import sys
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

def validate_and_add(item,schema,list):
  validate(item, schema=schema)
  list.append(item)

def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    final_list=[]
    for x in unique_list:
        final_list.append(str(np.unique(x))[1:-1].replace("'", ""))
    return final_list

def cleanname(name):
    name = str(name).replace('""', '')
    name = str(name).replace('""', '')
    name = str(name).replace('"', '')
    name = str(name).replace("#", '')
    name = str(name).replace(";", '')
    return name

def readips(rutatolog):
    reader=open(rutatolog, 'r')
    listahosts = []
    for line in reader:
        jsonreader = json.loads(line)
        listahosts.append(jsonreader['id.orig_h'])
        listahosts.append(jsonreader['id.resp_h'])
    listaips=unique(listahosts)
    return listaips

def knownservices(ips,rutatolog):

    #Leemos el json de los known_services
    try:
        reader = open(rutatolog, 'r')
        lines=[]
        for line in reader:
            row = json.loads(line)
            lines.append(row)

        # Para cada una de las lineas, se busca si coincide la IP y se registran los servicios
        finallist=[]
        for x in ips:

            serviceslist=[]
            ipandservice=[]
            for row in lines:
                if row['host'] == str(x):
                    if(len(str(row['service']))<100): #Para eliminar basura
                        serviceslist.append(row['service'][0])
            ipandservice=[x,serviceslist]
            finallist.append(ipandservice)
        return finallist
    except OSError as e:
        finallist = []
        for x in ips:
            serviceslist = []
            ipandservice = []
            ipandservice = [x, serviceslist]
            finallist.append(ipandservice)
        return finallist

def software(ips,rutatolog):
    try:
        reader = open(rutatolog, 'r')
        lines = []
        for line in reader:
            row = json.loads(line)
            lines.append(row)

        finallist = []
        finallist2=[]
        for x in ips:
            softwarelist = []
            oslist = []
            ipsandos = []
            ipsandsoftware = []
            for row in lines:
                if row['host'] == x:
                    name=row['unparsed_version']
                    name=cleanname(name)
                    if ("ubuntu" in str(np.unique(str(row['unparsed_version']))))or ("Ubuntu" in str(np.unique(str(row['unparsed_version'])))) or ("Debian" in str(np.unique(str(row['unparsed_version'])))):
                        oslist.append("Linux")
                    elif ("Windows" in str(np.unique(str(row['unparsed_version'])))):
                        oslist.append("Windows")
                    if (len(name) < 100):
                        softwarelist.append(str(np.unique(name)[0]))

            ipsandsoftware=[x,softwarelist]
            ipsandos=[x,oslist]
            finallist.append(ipsandsoftware)
            finallist2.append(ipsandos)
        return finallist,finallist2
    except OSError as e:
        finallist = []
        softwarelist=[]
        oslist=[]
        for x in ips:
            ipsandsoftware = [x, softwarelist]
            ipsandos = [x, oslist]
            finallist.append(ipsandsoftware)
            finallist2.append(ipsandos)
        return finallist, finallist2

def ja3reader(ips,rutatolog):
    try:
        reader = open(rutatolog, 'r')
        lines=[]
        for line in reader:
            row = json.loads(line)
            lines.append(row)

        # Para cada una de las lineas, se busca si coincide la IP y se registran los servicios
        finallist=[]
        for x in ips:

            ja3list=[]
            ipandja3=[]
            for row in lines:
                if row['id.orig_h'] == str(x):
                    ja3list.append(row['ja3'])
            #print(ja3list)
            ipandja3=[x,unique(ja3list)]
            finallist.append(ipandja3)
        return finallist
    except OSError as e:
        finallist = []
        for x in ips:
            ja3list = []
            ipandja3 = []
            ipandja3 = [x, ja3list]
            finallist.append(ipandja3)
        return finallist

def p0freader(ips,rutatolog):
    try:
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
                            os.append(fields[4].split('=')[1])
                        ipandos = [ip, os]
                        finallist.append(ipandos)
                if fields[3] == 'subj=srv':
                    os = []
                    ip = fields[2].split('=')[1].split('/')[0]
                    if 'os' in fields[4]:
                        if '???' in fields[4]:
                            os = []

                        else:
                            os.append(fields[4].split('=')[1])
                        ipandos=[ip,os]
                        finallist.append(ipandos)
            return finallist
    except OSError as e:
        finallist = []
        for x in ips:
            oslist = []
            ipandos = []
            ipandos = [x, oslist]
            finallist.append(ipandos)
        return finallist

def ja3lookup(ja3fing):
    useragents=[]
    for user in ja3fing:
        response = requests.get('https://ja3er.com/search/' + user)
        listuseragent = response.json()
        for item in listuseragent:
            if 'User-Agent' in item:
                useragents.append(cleanname(item['User-Agent']))
    return useragents

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
os.system("export PATH=/usr/local/zeek/bin:$PATH && cd "+dir+" && zeek -Cr "+dir+"*.pcap local")
os.system("p0f -r "+dir+"*.pcap -o "+dir+"p0f.log > /dev/null")

listaips=readips(dir+'conn.log')
listaservicios=knownservices(listaips,dir+'known_services.log')
listasoftware,listasos=software(listaips,dir+'software.log')
ja3 = ja3reader(listaips,dir+'ssl.log')
p0f = p0freader(listaips,dir+'p0f.log')

network=[]
for ip in listaips:
    if ip not in ['255.255.255.255','0.0.0.0','::']:
        for dev in listasos:
            if dev[0]==ip:
                operative=unique(dev[1])
        for dev in p0f:
            if dev[0]==ip:
                operative=unique(dev[1])
        for dev in listaservicios:
            if dev[0]==ip:
                services=dev[1]
        for dev in listasoftware:
            if dev[0]==ip:
                software=dev[1]
        for dev in ja3:
            if dev[0]==ip:
                ja3fing=dev[1]
        for dev in ja3:
            if dev[0]==ip:
                ja3fing=dev[1]
                useragents=ja3lookup(ja3fing)

        active={
            "IP":ip,
            "OS":operative,
            "Services":services,
            "Software":software,
            "JA3_Fingeprint":ja3fing,
            "Possible User-Agent":useragents
        }
        validate_and_add(active,schema,network)

writedata(dir,network)
os.system("cat "+dir+"data.json > "+cwd+"/templates/data.json")
tmp = os.popen("ls "+dir+"*.pcap").read()
command ="./brassfork -nodes="+dir+"nodes.csv -edges="+dir+"edges.csv"+" -in="+tmp
os.system("cd "+cwd+"&& "+command)
os.system("sed 's/,/"+"\t"+"/g' "+dir+"nodes.csv"+" > "+dir+"finalnodes.csv")
os.system("sed 's/,/"+"\t"+"/g' "+dir+"edges.csv"+" > "+dir+"finaledges.csv")
os.system("tr '[:upper:]' '[:lower:]' <"+dir+"finaledges.csv >"+dir+"outputedges.csv")
os.system("tr '[:upper:]' '[:lower:]' <"+dir+"finalnodes.csv >"+dir+"outputnodes.csv")
os.system("python3 convCSVtoGEXF.py -n "+dir+"outputnodes.csv -e "+dir+"outputedges.csv -d "+cwd+"/definitions.txt")
os.system("mv "+cwd+"/out.gexf "+dir)
os.system("rm "+dir+"*.csv")