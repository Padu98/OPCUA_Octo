import asyncio
import logging
import sys
sys.path.insert(0, "..")
from asyncua import Client, Node, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

#logging.basicConfig(level=logging.INFO)
#_logger = logging.getLogger("asyncua")

cert_idx = 1
cert = 'certs/client_certificate.pem'
private_key = 'certs/private_key_client.pem'


async def task(loop):
    url = "opc.tcp://192.168.2.140:4840/Octoprint"
    client = Client(url=url)
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=cert,
        private_key=private_key,
        server_certificate="certs/certificate.pem"
    )
    async with client:
        objects = client.nodes.objects
       # child = await objects.get_child(['1:Job_Operations', '1:Job_Operations'])
        obj = await client.nodes.root.get_child(["0:Objects", "1:Job_Operations"])
        obje = await client.nodes.root.get_child(["0:Objects", "1:Access_Control"])

#        res = await obj.call_method("1:start", "0212974DC0324BC6A437ACD87FDB772B")
 #       print(res)
        apikey = '10212974DC0324BC6A437ACD87FDB772B'
        res = await obje.call_method("1:addUser", str(apikey), "philipps", "chelsea", True, True)
        print(res)

#        print(await child.get_value())
 #       await child.set_value("new val")
 #       print(await child.get_value())


def main():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(task(loop))
    loop.close()


if __name__ == "__main__":
    main()