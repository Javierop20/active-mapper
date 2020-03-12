import numpy as np
import json
from jsonschema import *

schema = {
    "type" : "object",
    "properties":{
        "IP": {"type" : "string"},
        "OS": {"type":["string","array"]},
        "Services":{"type":["string","array"]},
        "Software":{"type":["string","array"]},
        "JA3_Fingerprint":{"type":["string","array"]}
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

def readips(rutatolog):
    reader=open(rutatolog, 'r')
    listahosts = []
    for line in reader:
        jsonreader = json.loads(line)
        listahosts.append(jsonreader['id.orig_h'])
    listaips=unique(listahosts)
    return listaips

def knownservices(ips,rutatolog):

    #Leemos el json de los known_services
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
                    serviceslist.append(row['service'])
        ipandservice=[x,serviceslist]
        finallist.append(ipandservice)
    return finallist

def software(ips,rutatolog):
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
                if ("ubuntu" in str(np.unique(str(row['unparsed_version']))))or ("Ubuntu" in str(np.unique(str(row['unparsed_version'])))) or ("Debian" in str(np.unique(str(row['unparsed_version'])))):
                    oslist.append("Linux")
                elif ("Windows" in str(np.unique(str(row['unparsed_version'])))):
                    oslist.append("Windows")
                else:
                    oslist.append("Unknown")
                softwarelist.append(str(np.unique(str(row['unparsed_version']))))

        ipsandsoftware=[x,softwarelist]
        ipsandos=[x,oslist]
        finallist.append(ipsandsoftware)
        finallist2.append(ipsandos)
    return finallist,finallist2

def ja3reader(ips,rutatolog):

    #Leemos el json de los known_services
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
dir = input("Introduce the base directory where the logs are: ")
dir = "/home/javier/Escritorio/prueba3/"
listaips=readips(dir+'conn.log')
listaservicios=knownservices(listaips,dir+'known_services.log')
listasoftware,listasos=software(listaips,dir+'software.log')
ja3 = ja3reader(listaips,dir+'ssl.log')

network=[]
for ip in listaips:
    for dev in listasos:
        if dev[0]==ip:
            os=dev[1]
            if(("Unknown" in dev[1])and (len(dev[1])>1)):
                os=dev[1].remove("Unknown")
            if(os==None):
                os=["Unknown"]

    for dev in listaservicios:
        if dev[0]==ip:
            services=dev[1]
    for dev in listasoftware:
        if dev[0]==ip:
            software=dev[1]
    for dev in ja3:
        if dev[0]==ip:
            ja3fing=dev[1]
    active={
        "IP":ip,
        "OS":os,
        "Services":services,
        "Software":software,
        "JA3_Fingeprint":ja3fing
    }
    validate_and_add(active,schema,network)
    print(active)

exit()