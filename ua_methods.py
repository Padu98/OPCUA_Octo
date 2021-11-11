from opcua import ua, uamethod, Server
import requests


########################## adcess control

@uamethod
def add_user(parent, api_key, username, passw, active, admin):
    headers = {'X-Api-Key' : api_key}
    data = {'name' : username,
            'password' : passw,
            'active' : active,
            'admin' : admin}
    requestString = 'http://localhost:5000/api/users/' 
    http_get_result = requests.put(requestString, headers=headers, data=data)
@uamethod
def del_user(parent, api_key, username):
    headers = {'X-Api-Key' : api_key}
   # data = {'app' : 'aaaaa'}
    requestString = 'http://localhost:5000/api/' + username
    http_get_result = requests.delete(requestString, headers=headers)

############################ connections handling    ************************
@uamethod
def con(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'connect',
            'port': '',
            'baudrate': 115200,
            'printerProfile': '',
            'save': True,
            'autoconnect' : True}
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print("Calling log_in")
@uamethod
def discon(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'disconnect'}
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print("Calling log_in")

######################### general information 

@uamethod
def log_in(parent, api_key, user, passw):
    headers = {'X-Api-Key' : api_key}
    data = { 'user' : user,
             'pass' : passw,
             'remember' : True}            ###not sure if parameter is set correct
    requestString = 'http://localhost:5000/api/login'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print("Calling log_in")
@uamethod
def Log_out(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/logout'
    http_get_result = requests.post(requestString, headers=headers)

######################### general information

#########################job Operations

@uamethod
def start_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'start'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def cancel_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'cancel'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def restart_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'restart'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def resume_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'pause', 'action' : 'resume'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def pause_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'pause', 'action' : 'pause'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)

#########################job Operations

#########################printer Operatioins

@uamethod
def home_head(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'home', 'axes' : ['x', 'y']}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def move_head(parent, api_key, x, y, z):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'jog',
            'x' : x,
            'y' : y, 
            'z' : z}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)
@uamethod
def set_feedrate_head(parent, api_key, n):
    data = {'command' : 'feedrate', 'factor' : n}
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)