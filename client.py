from os import name
from opcua import Client
from opcua import ua
import requests
import json



if __name__ == "__main__":
    #logging.basicConfig(level=logging.WARN)
 

    client = Client("opc.tcp://192.168.2.140:4840/Octoprint")
    #client.set

    client.set_security_string("Basic256Sha256,SignAndEncrypt,certs/client_certificate.pem,certs/private_key_client.pem")
    #client.set_security_string("Basic256Sha256,SignAndEncrypt,certs/server_certificate.pem,certs/server_private_key.pem")

   # client.load_private_key('certs/private_key_client.pem')

    print("success")
    input('Press Enter to continue ... ')
   

    try:
        print('still alive')
        client.connect()
        print('still alive')
        client.load_type_definitions()

        apiKey = '0212974DC0324BC6A437ACD87FDB772B'

        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()  #con server???
        print("Objects node is: ", objects)

        accessControl = objects.get_child('1:Access_Control')
        connectionHandling = objects.get_child('1:General_Information')

        res = accessControl.call_method('1:addUser', apiKey, 'philipp', 'chelsea', True,  True)
        print(res)
        res = connectionHandling.call_method('1:log_in', apiKey, 'philipp', 'chelsea')  
        print(res)
        res = accessControl.call_method('1:deleteUser', apiKey, 'philipp')
        print(res)

    finally:
       client.disconnect()
     