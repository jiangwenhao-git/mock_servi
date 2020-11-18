import xmltodict
import requests
import socket






with open('testcase.xml') as fd:
    doc = xmltodict.parse(fd.read())
    serviceAdr = doc['soap:Envelope']['soap:Header']['s:ReqHeader']['d:ServiceAdr']
    serviceAction  = doc['soap:Envelope']['soap:Header']['s:ReqHeader']['d:ServiceAction']
    serviceAction = serviceAction[5:]
    print("doc :"+str(doc))
    print("returnMsg :" + str(serviceAdr))
    print("returnCode :" + str(serviceAction))





