from zat import bro_log_reader
import numpy as np
import json
from collections import defaultdict

def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    final_list=[]
    for x in unique_list:
        final_list.append(str(np.unique(x))[1:-1].replace("'", ""))
    return final_list

def leer(rutatolog):
    reader = bro_log_reader.BroLogReader(rutatolog)
    listahosts=[]
    for row in reader.readrows():
        listahosts.append(row['id.orig_h'])
    listaips=unique(listahosts)
    return listaips
def knownservices(ips,rutatolog):
    reader = bro_log_reader.BroLogReader(rutatolog)
    finallist=[]
    for x in ips:
        serviceslist=[]
        ipandservice=[]
        for row in reader.readrows():
            if row['host']==x:
                print(str(row['service'])+": "+str(x))
                serviceslist.append(str(row['service']))
        ipandservice=[x,serviceslist]
        finallist.append(ipandservice)
    return finallist
def software(ips,rutatolog):
    reader = bro_log_reader.BroLogReader(rutatolog)
    finallist = []
    finallist2=[]
    for x in ips:
        softwarelist = []
        oslist = []
        ipsandos = []
        ipandsoftware = []
        for row in reader.readrows():
            if row['host'] == x:
                if ("ubuntu" in str(np.unique(str(row['unparsed_version']))))or ("Ubuntu" in str(np.unique(str(row['unparsed_version'])))) or ("Debian" in str(np.unique(str(row['unparsed_version'])))):
                    oslist.append("Linux")
                elif ("Windows" in str(np.unique(str(row['unparsed_version'])))):
                    oslist.append("Windows")

                softwarelist.append(str(np.unique(str(row['unparsed_version']))))
        ipandsoftware=[x,softwarelist]
        ipandos=[x,oslist]
        finallist.append(ipandsoftware)
        finallist2.append(ipandos)
    return finallist,finallist2
dir = input("Introduce the base directory where the logs are: ")
listaips=leer(dir+'/conn.log')
listaservicios=knownservices(listaips,dir+'/known_services.log')
listasoftware,listasos=software(listaips,'/software.log')
#/home/javier/Escritorio/prueba
final=json.dumps(listaservicios,indent=2)
parseado2=json.dumps(listasoftware,indent=2)
exit()