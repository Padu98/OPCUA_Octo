import os
from fileinput import filename
from importlib.resources import path
from pip import main
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult, Twin

ApplicationKeys = {"0212974DC0324BC6A437ACD87FDB772B"}
iothub_connection_str = "HostName=conFa-hub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=gQ5uwKeRCbU37S/AooNz0EICwauXsv0mePDb9SHBVbQ="
notvalid = True
device_id = "test/modules/opcmodul"
method_name1 = "uploadFile"
method_name2 = "selectFile"
method_name31 = "startJob"
method_name32 = "cancelJob"
method_name33 = "pauseJob"
method_name34 = "resumeJob"
method_name4 = "getValue"
method_name5 = "deleteFile"

def main(key):
    print("[0] delete file.")
    print("[1] upload file.")
    print("[2] select file.")
    print("[3] enter the Job Console.")
    print("[4] request specific node-value\n")
    print("press Ctrl + c to quit the opc-console.\n")

    inputString = input("Enter your command: ")
    print("\n")

    if(str(inputString)=="1"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("To Upload a File you need to provide the following Information: \n")
        url = input("url: ")
        print("\n")
        filename = input("filename:")
        print("\n")
        try:
            payload = {"key":key, "url":url, "filename":filename}
            registry_manager = IoTHubRegistryManager(iothub_connection_str)
            deviceMethod = CloudToDeviceMethod(method_name="uploadFile", payload=payload)
            response = registry_manager.invoke_device_method(device_id, deviceMethod)
            print("The Response was: ")
            print(response)
            print("\n")
        except Exception as e:
            print("Unexprected error {0}".format(e))
            
    elif(str(inputString)=="2"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("To select a file yout nee to provide the following information: \n")
        file = input("name: ")
        print("\n")
        location = input("location:")
        #print("\n")
        start = False
        x = input("type yes if the job should be started after the select process: ")
        if x == "yes":
            start = True
        print("\n")
        try:
            payload = {"key":key, "file": file , "location":location, "start":start}
            registry_manager = IoTHubRegistryManager(iothub_connection_str)
            deviceMethod = CloudToDeviceMethod(method_name=method_name2, payload=payload)
            response = registry_manager.invoke_device_method(device_id, deviceMethod)
            print("The Response was: ")
            print(response)
            print("\n")
        except Exception as e:
            print("Unexprected error {0}".format(e))
    elif(str(inputString)=="0"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("To delete a file yout nee to provide the following information: \n")
        location = input("location: ")
        print("\n")
        path = input("path:")
        print("\n")
        try:
            payload = {"key":key, "location": location , "path":path}
            registry_manager = IoTHubRegistryManager(iothub_connection_str)
            deviceMethod = CloudToDeviceMethod(method_name=method_name5, payload=payload)
            response = registry_manager.invoke_device_method(device_id, deviceMethod)
            print("the response was: ")
            print(response)
            print("\n")
        except Exception as e:
            print("unexprected error {0}".format(e))

    elif(str(inputString)=="3"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("the following job-operations are available: \n" )
        jobActive = True
        while jobActive:
            print("[1] start the selected job.")
            print("[2] cancel the current job.")
            print("[3] pause the current job.")
            print("[4] resume to the current job.")
            print("[5] leave job-operations menu\n")

            next_command = input("enter your command: ")

            if(next_command=="1"):
                os.system('cls' if os.name == 'nt' else 'clear')
                payload = {"key": key}
                try:
                    registry_manager = IoTHubRegistryManager(iothub_connection_str)
                    deviceMethod = CloudToDeviceMethod(method_name=method_name31, payload=payload)
                    response = registry_manager.invoke_device_method(device_id, deviceMethod)
                    print("the response was: ")
                    print(response)
                    print("\n")
                except Exception as e:
                    print("unexprected error {0}".format(e))
            elif(next_command=="2"):
                os.system('cls' if os.name == 'nt' else 'clear')
                payload = {"key": key}
                try:
                    registry_manager = IoTHubRegistryManager(iothub_connection_str)
                    deviceMethod = CloudToDeviceMethod(method_name=method_name32, payload=payload)
                    response = registry_manager.invoke_device_method(device_id, deviceMethod)
                    print("the response was: ")
                    print(response)
                    print("\n")
                except Exception as e:
                    print("unexprected error {0}".format(e))
            elif(next_command=="3"):
                os.system('cls' if os.name == 'nt' else 'clear')
                payload = {"key": key}
                try:
                    registry_manager = IoTHubRegistryManager(iothub_connection_str)
                    deviceMethod = CloudToDeviceMethod(method_name=method_name33, payload=payload)
                    response = registry_manager.invoke_device_method(device_id, deviceMethod)
                    print("the response was: "+ response.data)
                    print(response.status)
                    print("\n")
                except Exception as e:
                    print("unexprected error {0}".format(e))
            elif(next_command=="4"):
                os.system('cls' if os.name == 'nt' else 'clear')
                payload = {"key": key}
                try:
                    registry_manager = IoTHubRegistryManager(iothub_connection_str)
                    deviceMethod = CloudToDeviceMethod(method_name=method_name34, payload=payload)
                    response = registry_manager.invoke_device_method(device_id, deviceMethod)
                    print("the response was: "+response.data)
                    print(response.status)
                    print("\n")
                except Exception as e:
                    print("unexprected error {0}".format(e))
            elif(next_command=="5"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("returning back to main menu \n")
                jobActive = False
            else:
                print("no valid command. closing job operation console.")
    elif(str(inputString)=="4"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("to request a value you need to provide the following information: \n")
        parentnode = input("parent-node: ")
        print("\n")
        node = input("node:")
        print("\n")
        try:
            payload = {"parentnode": parentnode , "node":node}
            registry_manager = IoTHubRegistryManager(iothub_connection_str)
            deviceMethod = CloudToDeviceMethod(method_name=method_name4, payload=payload)
            response = registry_manager.invoke_device_method(device_id, deviceMethod)
            print("The Response was: ")
            print(response)
            print("\n")
        except Exception as e:
            print("unexprected error {0}".format(e))
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("command not known. returning back to start screen.")


if __name__=="__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("starting the opc-console. To continue you need a valid octoprint applicaion-key.")
    inputKey = ""
    while(notvalid):
        inputKey = input("Enter your key: ")
        if inputKey not in ApplicationKeys:
            print("the key is not valid. try again!")
        else:
            notvalid = False
    
    print("key validation was successfully. \n")
    print("the following methods are implemented: \n")
    while True:
        main(inputKey)