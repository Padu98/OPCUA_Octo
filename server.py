
import asyncio
import time
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


api_key='0212974DC0324BC6A437ACD87FDB772B' #Octoprint Application key

async def var_update(var, requestString):
    headers = {'X-Api-Key' : api_key}
    http_get_result = requests.get(requestString, headers=headers)
    if http_get_result.status_code == 200:
        await var.set_value(http_get_result.text)
 #       vals = await var.get_value()
#        print(vals)
#    print(http_get_result)

async def var_update2(var):
    oldval = await var.get_value()
    newval = oldval + '1'
    await var.set_value(newval)


model_filepath = 'opcuaServer.xml'


async def main():
    cert_user_manager = CertificateUserManager()
    await cert_user_manager.add_user('certs/client_certificate.pem', name='test_user')
    await cert_user_manager.add_user('certs/opcua_publisher_certificate.der', name='publisher')
    await cert_user_manager.add_user('certs/iiotcerts/8C7A.der', name='iiotuser1')
    await cert_user_manager.add_user('certs/iiotcerts/909B.der', name='iiotuser2')
    await cert_user_manager.add_user('certs/iiotcerts/mount_F7C0E.der', name='opc_publisher')

    server = Server(user_manager = cert_user_manager)
    await server.init()

    server.set_endpoint('opc.tcp://0.0.0.0:4840/Octoprint')
    server.set_server_name('Octoprint')

    server.set_security_policy([
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ], permission_ruleset = MyRoleRuleset())

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

    async def getVal(parent, parent_node, node):
      nodes = server.get_objects_node()
      parent =  await nodes.get_child(parent_node.Value)
      child = await parent.get_child(node.Value)
      val = await child.get_value()
      print("get_val")
      return [ua.Variant(val, ua.VariantType.String)]

    ##################################################Funktionen initialisieren
    get_val = await serverAndVersionInfo.get_child('1:get_val')
    server.link_method(get_val, getVal)

    addUser = await accessControl.get_child('1:addUser')
    deleteUser = await accessControl.get_child('1:deleteUser')
    server.link_method(addUser, add_user)
    server.link_method(deleteUser, del_user)

    selectFile = await fileOperations.get_child('1:select_file')
    server.link_method(selectFile, select_file)
    uploadFile = await fileOperations.get_child('1:upload_file')
    server.link_method(uploadFile, upload_file)
    deleteFile = await fileOperations.get_child('1:delete_file')
    server.link_method(deleteFile, delete_file)

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
#    server.link_method(getCurrentJob, test)          #################* muss noch angepasst werden

    printerHead = await printerOperations.get_child('1:Printer_Head')
    home = await printerHead.get_child('1:home')
    jog = await printerHead.get_child('1:jog')
    setFeedRate = await printerHead.get_child('1:set_feed_rate')
    server.link_method(home, home_head)
    server.link_method(jog, move_head)
    server.link_method(setFeedRate, set_feedrate_head)


    ##################################################werte initialisieren

    connectionSettings = await connectionHandling.get_child('1:Settings')
    await connectionSettings.set_writable()
    allFiles = await fileOperations.get_child('1:All_Files')
    currentUser = await generalInfos.get_child('1:currentuser')
    printerState = await printerOperations.get_child('1:Printer_State')
    printerTemperature = await printerOperations.get_child('1:Printer_Temperature')
    serverInfos = await serverAndVersionInfo.get_child('1:Server_Information')
    await serverInfos.set_writable()
    versionInfos = await serverAndVersionInfo.get_child('1:Version_Information')
    await versionInfos.set_writable()
    jobInfos = await JobOperations.get_child('1:Job_Information')

    await connectionSettings.set_value('empty')
    await allFiles.set_value('empty')
    await currentUser.set_value('empty')
    await printerState.set_value('empty')
    await serverInfos.set_value('empty')
    await printerTemperature.set_value('empty')
    await versionInfos.set_value('empty')
    await jobInfos.set_value('empty')

    ##################################################werte initialisieren ende


   # vup1 = VarUpdater(connectionSettings, 'http://localhost:5000/api/connection')
   # vup2 = VarUpdater(allFiles, 'http://localhost:5000/api/files')
   # vup3 = VarUpdater(currentUser, 'http://localhost:5000/api/currentuser')
   # vup4 = VarUpdater(printerState, 'http://localhost:5000/api/printer?exclude=temperature,sd')
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
            await asyncio.sleep(20)
            await var_update(serverInfos, 'http://localhost:5000/api/server')
            await var_update(versionInfos, 'http://localhost:5000/api/version')
            await var_update(jobInfos, 'http://localhost:5000/api/job')
            await var_update(allFiles, 'http://localhost:5000/api/files')
            await var_update(printerState, 'http://localhost:5000/api/printer?exclude=temperature,sd')
            await var_update(printerTemperature, 'http://localhost:5000/api/printer')




if __name__ == '__main__':
    asyncio.run(main())