import asyncio
from opcua.crypto import security_policies
from opcua.ua.uaprotocol_auto import UserNameIdentityToken
import requests
from threading import Thread
from opcua.server.user_manager import UserManager
from ua_methods import *
from permission_ruleset import MyRoleRuleset

from asyncua import ua, uamethod, Server
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server.user_managers import CertificateUserManager



async def var_update(var, requestString):
    headers = {'X-Api-Key' : api_key}
    http_get_result = requests.get(requestString, headers=headers)
    if http_get_result.status_code == 200:
        await var.set_value(http_get_result.text)


api_key='0212974DC0324BC6A437ACD87FDB772B'
model_filepath = 'opcuaServer.xml'


class OPC_Server:

    async def init(self):
        cert_user_manager = CertificateUserManager()
        await cert_user_manager.add_user('certs/client_certificate.pem', name='test_user')
#        await cert_user_manager.add_user('certs/opcua_publisher_certificate.der', name='publisher')
   #     await cert_user_manager.add_user('certs/iiotcerts/8C7A.der', name='iiotuser1')
  #      await cert_user_manager.add_user('certs/iiotcerts/909B.der', name='iiotuser2')
 #       await cert_user_manager.add_user('certs/iiotcerts/mount_F7C0E.der', name='opc_publisher')

        self.server = Server(user_manager = cert_user_manager)
        await self.server.init()

        await self.init_server()
        await self.set_security()
        await self.initialize_methods()
        await self.initialize_nodes()


    async def set_security(self):
        self.server.set_security_policy([
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
              ], permission_ruleset = MyRoleRuleset())

        await self.server.load_private_key('certs/key.pem')
        await self.server.load_certificate('certs/certificate.pem')

    async def init_server(self):
        self.server.set_endpoint('opc.tcp://0.0.0.0:4840/Octoprint')
        self.server.set_server_name('Octoprint')
        await self.server.import_xml(model_filepath)
        self.nodes = self.server.get_objects_node()

    async def initialize_nodes(self):
        connectionHandling = await self.nodes.get_child('1:Connection_Handling')
        accessControl = await self.nodes.get_child('1:Access_Control')
        fileOperations = await self.nodes.get_child('1:File_Operations')
        generalInfos = await self.nodes.get_child('1:General_Information')
        JobOperations = await self.nodes.get_child('1:Job_Operations')
        printerOperations = await self.nodes.get_child('1:Printer_Operations')
        serverAndVersionInfo = await self.nodes.get_child('1:Server_Information')

        connectionSettings = await connectionHandling.get_child('1:Settings')
        await connectionSettings.set_writable()
        allFiles = await fileOperations.get_child('1:All_Files')
        await allFiles.set_writable()
        currentUser = await generalInfos.get_child('1:currentuser')
        await currentUser.set_writable()
        printerState = await printerOperations.get_child('1:Printer_State')
        await printerState.set_writable()
        printerTemperature = await printerOperations.get_child('1:Printer_Temperature')
        await printerTemperature.set_writable()
        serverInfos = await serverAndVersionInfo.get_child('1:Server_Information')
        await serverInfos.set_writable()
        versionInfos = await serverAndVersionInfo.get_child('1:Version_Information')
        await versionInfos.set_writable()
        jobInfos = await JobOperations.get_child('1:Job_Information')
        await jobInfos.set_writable()

        async with self.server:
            print('server start')
            while True:
                await asyncio.sleep(20)
                await var_update(serverInfos, 'http://localhost:5000/api/server')
                await var_update(versionInfos, 'http://localhost:5000/api/version')
                await var_update(jobInfos, 'http://localhost:5000/api/job')
                await var_update(allFiles, 'http://localhost:5000/api/files')
                await var_update(printerState, 'http://localhost:5000/api/printer?exclude=temperature,sd')
                await var_update(printerTemperature, 'http://localhost:5000/api/printer')

    async def initialize_methods(self):
        connectionHandling = await self.nodes.get_child('1:Connection_Handling')
        accessControl = await self.nodes.get_child('1:Access_Control')
        fileOperations = await self.nodes.get_child('1:File_Operations')
        generalInfos = await self.nodes.get_child('1:General_Information')
        JobOperations = await self.nodes.get_child('1:Job_Operations')
        printerOperations = await self.nodes.get_child('1:Printer_Operations')
        serverAndVersionInfo = await self.nodes.get_child('1:Server_Information')

        get_val = await serverAndVersionInfo.get_child('1:get_val')
#        self.server.link_method(get_val, getVal)

        addUser = await accessControl.get_child('1:addUser')
        deleteUser = await accessControl.get_child('1:deleteUser')
        self.server.link_method(addUser, add_user)
        self.server.link_method(deleteUser, del_user)

        selectFile = await fileOperations.get_child('1:select_file')
        self.server.link_method(selectFile, select_file)
        uploadFile = await fileOperations.get_child('1:upload_file')
        self.server.link_method(uploadFile, upload_file)
        deleteFile = await fileOperations.get_child('1:delete_file')
        self.server.link_method(deleteFile, delete_file)

        connect = await connectionHandling.get_child('1:connection_request')
        disconnect = await connectionHandling.get_child('1:disconnection_request')
        self.server.link_method(connect, con)
        self.server.link_method(disconnect, discon)

        logIn = await generalInfos.get_child('1:log_in')
        logOut = await generalInfos.get_child('1:log_out')
        self.server.link_method(logIn, log_in)
        self.server.link_method(logOut, Log_out)

        start = await JobOperations.get_child('1:start')
        cancel = await JobOperations.get_child('1:cancel')
        pause = await JobOperations.get_child('1:pause')
        restart = await JobOperations.get_child('1:restart')
        resume = await JobOperations.get_child('1:resume')
        self.server.link_method(start, start_job)
        self.server.link_method(cancel, cancel_job)
        self.server.link_method(pause, pause_job)
        self.server.link_method(restart, restart_job)
        self.server.link_method(resume, resume_job)

        printerHead = await printerOperations.get_child('1:Printer_Head')
        home = await printerHead.get_child('1:home')
        jog = await printerHead.get_child('1:jog')
        setFeedRate = await printerHead.get_child('1:set_feed_rate')
        self.server.link_method(home, home_head)
        self.server.link_method(jog, move_head)
        self.server.link_method(setFeedRate, set_feedrate_head)

    async def getVal(self, parent, parent_node, node):
        nodes = self.server.get_objects_node()
        parent =  await nodes.get_child(parent_node.Value)
        child = await parent.get_child(node.Value)
        val = await child.get_value()
        print("get_val")
        return [ua.Variant(val, ua.VariantType.String)]


async def function() -> asyncio.coroutine:
     opc_server = OPC_Server()
     await opc_server.init()


if __name__ == '__main__':
    asyncio.run(function())