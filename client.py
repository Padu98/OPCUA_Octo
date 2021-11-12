from os import name
from opcua import Client
from opcua import ua
import requests
import json



if __name__ == "__main__":
    #logging.basicConfig(level=logging.WARN)
 

    client = Client("opc.tcp://192.168.2.140:4840/Octoprint")

    try:
        client.connect()
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
     