from opcua import Client
from opcua import ua


if __name__ == "__main__":
    #logging.basicConfig(level=logging.WARN)
 

    client = Client("opc.tcp://localhost:4840/Octoprint")

    try:
        client.connect()
        client.load_type_definitions()

        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()  #con server???
        print("Objects node is: ", objects)

        connectionHandling = objects.get_child('1:Connection_Handling')
        print()

        res = connectionHandling.call_method('1:connection_request', 23)
        print(res)



    finally:
        client.disconnect()