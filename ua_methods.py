from opcua import ua, uamethod, Server
import requests
import json


########################## adcess control

@uamethod
def add_user(parent, api_key, username, passw, active, admin):
    headers = {'X-Api-Key' : api_key}
    data = {'name' : username,
            'password' : passw,
            'active' : active,
            'admin' : admin}
    requestString = 'http://localhost:5000/api/access/users' 
    print('calling add_user with data:')
    print(data)
    print(api_key)
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)

@uamethod
def del_user(parent, api_key, username):
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/access/users/' + username
    http_get_result = requests.delete(requestString, headers=headers)
    print(http_get_result)

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
    jsonData = json.dumps(data)
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, data=jsonData)
    print(http_get_result)
@uamethod
def discon(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'disconnect'}
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)

######################### general information 

@uamethod
def log_in(parent, api_key, user, passw):
    headers = {'X-Api-Key' : api_key}
    data = { 'user' : user,
             'pass' : passw,
             'remember' : True}            ###not sure if parameter is set correct
    requestString = 'http://localhost:5000/api/login'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def Log_out(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/logout'
    http_get_result = requests.post(requestString, headers=headers)
    print(http_get_result)

######################### general information

#########################job Operations

@uamethod
def start_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'start'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def cancel_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'cancel'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def restart_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'restart'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def resume_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'pause', 'action' : 'resume'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def pause_job(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'pause', 'action' : 'pause'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)

#########################job Operations

#########################printer Operatioins

@uamethod
def home_head(parent, api_key):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'home', 'axes' : ['x', 'y']}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def move_head(parent, api_key, x, y, z):
    headers = {'X-Api-Key' : api_key}
    data = {'command' : 'jog',
            'x' : x,
            'y' : y, 
            'z' : z}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)
@uamethod
def set_feedrate_head(parent, api_key, n):
    data = {'command' : 'feedrate', 'factor' : n}
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, data=data)
    print(http_get_result)