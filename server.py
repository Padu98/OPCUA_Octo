from opcua import ua, uamethod, server
import time 
import requests
from threading import Thread
from ua_methods import *

api_key='' #Octoprint Application key

class VarUpdater(Thread):
    def __init__(self, var, requestString):
        Thread.__init__(self)
        self._stopev = False
        self.var = var
        self.requestString = requestString

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            headers = {'X-Api-Key' : api_key}
            http_get_result = requests.get(self.requestString, headers=headers)
            if http_get_result.status_code == 200:   #200 als string oder int
                self.var.set_value(http_get_result.text)  ##ergebnis im json format
                print(http_get_result)
            time.sleep(30)
   
@uamethod
def test(value):
    print("das ist ein Test")
    return value

model_filepath = "opcuaServer.xml"


if __name__ == '__main__':
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/Octoprint")
    server.set_server_name("Octoprint")

    server.import_xml(model_filepath)


    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])


    nodes = server.get_objects_node()


    connectionHandling = nodes.get_child('1:Connection_Handling')
    accessControl = nodes.get_child('1:Access_Control')
    fileOperations = nodes.get_child('1:File_Operations')
    generalInfos = nodes.get_child('1:General_Information')
    JobOperations = nodes.get_child('1:Job_Operations')
    printerOperations = nodes.get_child('1:Printer_Operations')
    serverAndVersionInfo = nodes.get_child('1:Server_Information')

   

    ##################################################Funktionen initialisieren
    addUser = accessControl.get_child('1:addUser')
    deleteUser = accessControl.get_child('1:deleteUser')
    server.link_method(addUser, add_user)
    server.link_method(deleteUser, del_user)

    connect = connectionHandling.get_child('1:connection_request')
    disconnect = connectionHandling.get_child('1:disconnection_request')
    server.link_method(connect, test)           #eigentlich con
    server.link_method(disconnect, discon)

    logIn = generalInfos.get_child('1:log_in')
    logOut = generalInfos.get_child('1:log_out')
    server.link_method(logIn, log_in)
    server.link_method(logOut, Log_out)

    start = JobOperations.get_child('1:start')
    cancel = JobOperations.get_child('1:cancel')
    pause = JobOperations.get_child('1:pause')
    restart = JobOperations.get_child('1:restart')
    resume = JobOperations.get_child('1:resume')
    getCurrentJob = JobOperations.get_child('1:currentJob')
    server.link_method(start, start_job)
    server.link_method(cancel, cancel_job)
    server.link_method(pause, pause_job)
    server.link_method(restart, restart_job)
    server.link_method(resume, resume_job)
    server.link_method(getCurrentJob, test)          #################* muss noch angepasst werden

    printerHead = printerOperations.get_child('1:Printer_Head')
    home = printerHead.get_child('1:home')
    jog = printerHead.get_child('1:jog')
    setFeedRate = printerHead.get_child('1:set_feed_rate')
    server.link_method(home, home_head)
    server.link_method(jog, move_head)
    server.link_method(setFeedRate, set_feedrate_head)


    ##################################################werte initialisieren

    connectionSettings = connectionHandling.get_child('1:Settings')
    allFiles = fileOperations.get_child('1:All_Files')
    currentUser = generalInfos.get_child('1:currentuser')
    printerState = printerOperations.get_child('1:Printer_State')
    serverInfos = serverAndVersionInfo.get_child('1:Server_Information')
    versionInfos = serverAndVersionInfo.get_child('1:Version_Information')

    connectionSettings.set_value('uninitialized')
    connectionSettings.set_read_only()
    allFiles.set_value('uninitialized')
    allFiles.set_read_only()
    currentUser.set_value('uninitialized')
    currentUser.set_read_only()
    printerState.set_value('uninitialized')
    printerState.set_read_only()
    serverInfos.set_value('uninitialized')
    serverInfos.set_read_only()
    versionInfos.set_value('uninitialized')
    versionInfos.set_read_only()

    ##################################################werte initialisieren ende

    server.start()

    #vup1 = VarUpdater(connectionSettings, 'http://localhost:5000/api/connection')
    #vup2 = VarUpdater(allFiles, 'http://localhost:5000/api/files')
    #vup3 = VarUpdater(currentUser, 'http://localhost:5000/api/currentuser')
    #vup4 = VarUpdater(printerState, '')
    #vup5 = VarUpdater(serverInfos, 'http://localhost:5000/api/server')
    #vup6 = VarUpdater(versionInfos, 'http://localhost:5000/api/version')

    #vup1.start()
    #vup2.start()
    #vup3.start()
    #vup4.start()
    #vup5.start()
    #vup6.start()

    try:
        print('Server Start')
        while True:
            True
       # server.set_attribute_value(myvar.nodeid, ua.DataValue(9.9))  # Server side write method which is a but faster than using set_value
    finally:
        #vup1.stop()
        #vup2.stop()
        #vup3.stop()
        #vup4.stop()
        #vup5.stop()
        #vup6.stop()
        server.stop()
