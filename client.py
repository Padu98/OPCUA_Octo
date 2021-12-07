from os import name
from opcua import Client
from opcua import ua
import requests
import json



if __name__ == "__main__":


    client = Client("opc.tcp://192.168.2.140:4840/Octoprint")
    client.set_security_string("Basic256Sha256,SignAndEncrypt,certs/client_certificate.pem,certs/private_key_client.pem")


#    client.set_user('user1')
#    client.set_password('pw12')

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
        serverInformation = objects.get_child('1:Server_Information')

        result = serverInformation.get_child('1:Server_Information')
        print(result.get_value())
#        res = accessControl.call_method('1:addUser', apiKey, 'philipp', 'chelsea', True,  True)
#        print(res)
#        res = connectionHandling.call_method('1:log_in', apiKey, 'philipp', 'chelsea')
#        print(res)
#        res = accessControl.call_method('1:deleteUser', apiKey, 'philipp')
#        print(res)

    finally:
       client.disconnect()





   


     
