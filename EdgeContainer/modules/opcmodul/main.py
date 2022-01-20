# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
from http import client
import imp
from pkgutil import ImpImporter
import sys
import signal
import threading
from unittest import result
from urllib import response
from azure.iot.device.aio import IoTHubModuleClient
import json
from azure.iot.device import MethodResponse

from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256


cert = 'certs/client_certificate.pem'
private_key = 'certs/private_key_client.pem'


# Event indicating client stop
stop_event = threading.Event()


def create_client():
    iotclient = IoTHubModuleClient.create_from_edge_environment()
    opcclient = Client(url="opc.tcp://192.168.2.140:4840/Octoprint")
    ##function for receiving method requests
    async def receive_methodrequest_handler(method):
        await opcclient.set_security(
            SecurityPolicyBasic256Sha256,
            certificate=cert,
            private_key=private_key,
            server_certificate="certs/certificate.pem"
        )

        if method.name == "startJob":
            if("key" in method.payload):
                com = "1:start"
                async with opcclient:
                    objects = opcclient.nodes.objects
                    child = await opcclient.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
                    res = await child.call_method(com, method.payload.get("key"))

                payload = {"data": "execute successfully"}
                method_response = MethodResponse.create_from_method_request(method, result, payload)
                await iotclient.send_method_response(method_response)
            else:
                payload = {"data": "key is missing"}
                method_response = MethodResponse.create_from_method_request(method, 400, payload)
                await iotclient.send_method_response()
        elif method.name == "pauseJob":
            if("key" in method.payload):
                com = "1:pause"
                async with opcclient:
                    objects = opcclient.nodes.objects
                    child = await opcclient.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
                    res = await child.call_method(com, method.payload.get("key"))

                payload = {"data": "execute successfully"}
                method_response = MethodResponse.create_from_method_request(method, result, payload)
                await iotclient.send_method_response(method_response)
            else:
                payload = {"data": "key is missing"}
                method_response = MethodResponse.create_from_method_request(method, 400, payload)
                await iotclient.send_method_response()
        elif method.name == "cancelJob":
            if("key" in method.payload):
                com = "1:cancel"
                async with opcclient:
                    objects = opcclient.nodes.objects
                    child = await opcclient.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
                    res = await child.call_method(com, method.payload.get("key"))

                payload = {"data": "execute successfully"}
                method_response = MethodResponse.create_from_method_request(method, result, payload)
                await iotclient.send_method_response(method_response)
            else:
                payload = {"data": "key is missing"}
                method_response = MethodResponse.create_from_method_request(method, 400, payload)
                await iotclient.send_method_response()
        elif method.name == "resumeJob":
            if("key" in method.payload):
                com = "1:resume"
                async with opcclient:
                    objects = opcclient.nodes.objects
                    child = await opcclient.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
                    res = await child.call_method(com, method.payload.get("key"))

                payload = {"data": "execute successfully"}
                method_response = MethodResponse.create_from_method_request(method, result, payload)
                await iotclient.send_method_response(method_response)
            else:
                payload = {"data": "key is missing"}
                method_response = MethodResponse.create_from_method_request(method, 400, payload)
                await iotclient.send_method_response()
        elif method.name == "resumeJob":
            if("key" in method.payload):
                com = "1:addUser"
                async with opcclient:
                    objects = opcclient.nodes.objects
                    child = await opcclient.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
                    res = await child.call_method(com, method.payload.get("key"), "philipps", "chelsea", True, True)

                payload = {"data": "execute successfully"}
                method_response = MethodResponse.create_from_method_request(method, result, payload)
                await iotclient.send_method_response(method_response)
            else:
                payload = {"data": "key is missing"}
                method_response = MethodResponse.create_from_method_request(method, 400, payload)
                await iotclient.send_method_response()

        else:        
            print("method could not be identified")
            payload = {"result": True, "data": "execute fail"}
            method_response = MethodResponse.create_from_method_request(method, 400, payload)
            await iotclient.send_method_response(method_response)


    try:
        iotclient.on_method_request_received = receive_methodrequest_handler
    except:
        iotclient.shutdown()
        raise

    return iotclient


async def run_sample(client):
    while True:
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
