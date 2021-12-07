import asyncio

import time
from opcua.crypto import security_policies
from opcua.ua.uaprotocol_auto import UserNameIdentityToken 
import requests
from threading import Thread
from opcua.server.user_manager import UserManager
from ua_methods import *

from asyncua import ua, uamethod, Server
from asyncua.crypto.permission_rules import SimpleRoleRuleset
from asyncua.server.users import UserRole
from asyncua.server.user_managers import CertificateUserManager


api_key='0212974DC0324BC6A437ACD87FDB772B' #Octoprint Application key

async def var_update(var, requestString):
    headers = {'X-Api-Key' : api_key}
    http_get_result = requests.get(requestString, headers=headers)
    if http_get_result.status_code == 200:
        await var.set_value(http_get_result.text)
        print(http_get_result)



#class VarUpdater(Thread):
#    def __init__(self, var, requestString):
#       	Thread.__init__(self)
#       	self._stopev = False
#       	self.var = var
#       	self.requestString = requestString

#    def stop(self):
#       	self._stopev = True

#    async def run(self):
#       	while not self._stopev:
#           headers = {'X-Api-Key' : api_key}
#           http_get_result = requests.get(self.requestString, headers=headers)
#           if http_get_result.status_code == 200:   
#               await self.var.set_value(http_get_result.text) 
#           time.sleep(15)


@uamethod
def test(parent):
    print('hallo das ist ein test')
   

model_filepath = 'opcuaServer.xml'


async def main():
    cert_user_manager = CertificateUserManager()
    await cert_user_manager.add_user('certs/client_certificate.pem', name='test_user')
    await cert_user_manager.add_user('certs/opcua_publisher_certificate.der', name='publisher')

    server = Server(user_manager = cert_user_manager)
    await server.init()

    server.set_endpoint('opc.tcp://0.0.0.0:4840/Octoprint')
    server.set_server_name('Octoprint')

    server.set_security_policy([
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ], permission_ruleset = SimpleRoleRuleset())


    await server.load_private_key('certs/key.pem')   
    await server.load_certificate('certs/certificate.pem')

    await server.import_xml(model_filepath)
    nodes = server.get_objects_node()


    connectionHandling = await nodes.get_child('1:Connection_Handling')
    accessControl = await nodes.get_child('1:Access_Control')
    fileOperations = await nodes.get_child('1:File_Operations')
    generalInfos = await nodes.get_child('1:General_Information')
    JobOperations = await nodes.get_child('1:Job_Operations')
    printerOperations = await nodes.get_child('1:Printer_Operations')
    serverAndVersionInfo = await nodes.get_child('1:Server_Information')

   

    ##################################################Funktionen initialisieren
    addUser = await accessControl.get_child('1:addUser')
    deleteUser = await accessControl.get_child('1:deleteUser')
    server.link_method(addUser, test)  ##fehlt
    server.link_method(deleteUser, del_user)

    connect = await connectionHandling.get_child('1:connection_request')
    disconnect = await connectionHandling.get_child('1:disconnection_request')
    server.link_method(connect, con)           
    server.link_method(disconnect, discon)

    logIn = await generalInfos.get_child('1:log_in')
    logOut = await generalInfos.get_child('1:log_out')
    server.link_method(logIn, log_in)
    server.link_method(logOut, Log_out)

    start = await JobOperations.get_child('1:start')
    cancel = await JobOperations.get_child('1:cancel')
    pause = await JobOperations.get_child('1:pause')
    restart = await JobOperations.get_child('1:restart')
    resume = await JobOperations.get_child('1:resume')
    getCurrentJob = await JobOperations.get_child('1:currentJob')
    server.link_method(start, start_job)
    server.link_method(cancel, cancel_job)
    server.link_method(pause, pause_job)
    server.link_method(restart, restart_job)
    server.link_method(resume, resume_job)
    server.link_method(getCurrentJob, test)          #################* muss noch angepasst werden

    printerHead = await printerOperations.get_child('1:Printer_Head')
    home = await printerHead.get_child('1:home')
    jog = await printerHead.get_child('1:jog')
    setFeedRate = await printerHead.get_child('1:set_feed_rate')
    server.link_method(home, home_head)
    server.link_method(jog, move_head)
    server.link_method(setFeedRate, set_feedrate_head)


    ##################################################werte initialisieren

    connectionSettings = await connectionHandling.get_child('1:Settings')
    allFiles = await fileOperations.get_child('1:All_Files')
    currentUser = await generalInfos.get_child('1:currentuser')
    printerState = await printerOperations.get_child('1:Printer_State')
    serverInfos = await serverAndVersionInfo.get_child('1:Server_Information')
    versionInfos = await serverAndVersionInfo.get_child('1:Version_Information')

    await connectionSettings.set_value('uninitialized')
    await connectionSettings.set_read_only()
    await allFiles.set_value('uninitialized')
    await allFiles.set_read_only()
    await currentUser.set_value('uninitialized')
    await currentUser.set_read_only()
    await printerState.set_value('uninitialized')
    await printerState.set_read_only()
    await serverInfos.set_value('uninitialized')
    await serverInfos.set_read_only()
    await versionInfos.set_value(1998.0)
    await versionInfos.set_read_only()

    ##################################################werte initialisieren ende


   # vup1 = VarUpdater(connectionSettings, 'http://localhost:5000/api/connection')
   # vup2 = VarUpdater(allFiles, 'http://localhost:5000/api/files')
   # vup3 = VarUpdater(currentUser, 'http://localhost:5000/api/currentuser')
   # vup4 = VarUpdater(printerState, 'http://localhost:5000/api/printer?history=false')
   # vup5 = VarUpdater(serverInfos, 'http://localhost:5000/api/server')
   # vup6 = VarUpdater(versionInfos, 'http://localhost:5000/api/version')

    #vup1.start()
    #vup2.start()
    #vup3.start()
   # vup4.start()
    #vup5.start()
    #vup6.start()

    async with server:
        print('server start')
        while True:
            await asyncio.sleep(30)
#            await var_update(printerState, 'http://localhost:5000/api/printer?history=false')
            await var_update(currentUser, 'http://localhost:5000/api/currentuser')




if __name__ == '__main__':
    asyncio.run(main())
