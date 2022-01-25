import os
import string
import json
import uuid
import time
from azure.storage.blob import ContainerClient, BlobClient
import ast
import requests

conString = ""
node_token2012 = 'YgtvyoSUCyXR0pKDCcDb'
node_token2013 = 'X2G5VfcocMKXgns5G8hc'
node_token2017 = 'IwSESR3zjOj3181v3JpN'
node_token2022 = 'kOYAcQMplURAjtSuSGih'
node_token2025 = 'QclBihMlarIh8K1kO4C5'
node_token3000 = 'IccBVuMqAmaYfxHxgMn4'

def startProcessing(text):
   # print('Processor started using path: ' + os.getcwd())

    container = ContainerClient.from_connection_string(conString, container_name="iothub-glpdei")
    blob_list = container.list_blobs()
    for blob in blob_list:
        if blob.size > 508: #smaller == empty
            print('Downloaded a non empty blob: ' + blob.name)
            blob_client = ContainerClient.get_blob_client(container, blob=blob.name)
            text = blob_client.download_blob().readall()
            text = str(text)
            container.delete_blob(blob.name) #delete blob after it is red
            break
    return text

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def converPrinterTemperature (dicti):
    if(dicti['restResult']['status'] == 'empty'):
        tool0 = {'actual0': 0, 'target0': 0, 'offset0':0}
        dicti['restResult']['tool0'] = tool0
        tool1 =  {'actual1': 0, 'target1': 0, 'offset1':0}
        dicti['restResult']['tool1'] = tool1
        tool2 = {'actual2': 0, 'target2': 0, 'offset2':0}
        dicti['restResult']['tool2'] = tool2
        bed =  {'actualb': 0, 'targetb': 0, 'offsetb':0}
        dicti['restResult']['bed'] = bed
            
    else:
        if  'tool0' in dicti.get('restResult'):
            tool0 = {'actual0': float(dicti.restResult.tool0.actual), 'target0':  float(dicti.restResult.tool0.target), 'offset0': float(dicti.restResult.tool0.offset)}
        else:
             tool0 = {'actual0': 0, 'target0': 0, 'offset0':0}
        dicti['restResult']['tool0'] = tool0

        if  'tool1' in dicti['restResult']:
            tool1 = {'actual1': float(dicti.restResult.tool1.actual), 'target1':  float(dicti.restResult.tool1.target), 'offset1': float(dicti.restResult.tool1.offset)}
        else:
             tool1 = {'actual1': 0, 'target1': 0, 'offset1':0}
        dicti['restResult']['tool1'] = tool1
        if  'tool2' in dicti['restResult']:
            tool2 = {'actual2': float(dicti.restResult.tool2.actual), 'target2':  float(dicti.restResult.tool2.target), 'offset2': float(dicti.restResult.tool2.offset)}
        else:
             tool2 = {'actual2': 0, 'target2': 0, 'offset2':0}
        dicti['restResult']['tool2'] = tool2
        if  'bed' in dicti['restResult']:
            bed = {'actualb': float(dicti.restResult.bed.actual), 'targetb':  float(dicti.restResult.bed.target), 'offsetb': float(dicti.restResult.bed.offset)}
        else:
             bed = {'actualb': 0, 'targetb': 0, 'offsetb':0}
        dicti['restResult']['bed'] = bed
        
    return dicti
        




if __name__ == '__main__':
    print("press Str + X to quit!")
    opcua_nodes = []
    while True:
        text = ''
        time.sleep(2)
        text = startProcessing(text)

        if len(text) > 0:
            firstIndex = text.index('{"OPCUANodes')
            text = text[firstIndex:]
            lastIndex = text.index('}]}]') +3

            resultString = text[:lastIndex]
            #print("text:   " +resultString)
            valDict = {}
            valDict = ast.literal_eval(resultString)

            if type(valDict) != tuple:
                tuples = (valDict,)
            else:
                tuples = valDict

            for elements in tuples:
                opcua_nodes = elements.get('OPCUANodes')

                for element in opcua_nodes:
                    if str(element).find('i=2012') != -1:
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token2012+'/telemetry' 
                        http_get_result = requests.post(requestString, json=element)
                        print(http_get_result)
                    elif str(element).find('i=2013') != -1:
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token2013+'/telemetry'  
                        http_get_result = requests.post(requestString, json=element)
                        print(http_get_result)
                    elif str(element).find('i=2017') != -1:
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token2017+'/telemetry'  
                        http_get_result = requests.post(requestString, json=element)
                        print(http_get_result)
                    elif str(element).find('i=2022') != -1:
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token2022+'/telemetry'  
                        http_get_result = requests.post(requestString, json=element)
                        print(http_get_result)
                    elif str(element).find('i=2025') != -1:
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token2025+'/telemetry'
                        http_get_result = requests.post(requestString, json=element) 
                        print(http_get_result)
                    elif str(element).find('i=3000') != -1:
                        element = converPrinterTemperature(element)
                        requestString = 'https://demo.thingsboard.io/api/v1/'+node_token3000+'/telemetry' 
                        http_get_result = requests.post(requestString, json=element)
                        print(http_get_result)
                    else:
                        print("no element found with given nodeid")


        

        