from opcua import ua, uamethod, Server
import requests
import os
import wget


async def getValTest(parent, parent_node, node):
    print(parent_node.Value)
    nodes = server.get_objects_node()
    parent = await nodes.get_child(parent_node)
    child = await parent.get_child(node)
    val = await child.get_value()
    print("get_val")
   # return val

########################## adcess control

@uamethod
def add_user(parent, api_key, username, passw, active, admin):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'name' : username,
            'password' : passw,
            'active' : active,
            'admin' : admin}
    requestString = 'http://localhost:5000/api/access/users'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print("called add_user")
    print(http_get_result)
    return http_get_result.status_code

@uamethod
def del_user(parent, api_key, username):
    headers = {'X-Api-Key' :api_key.Value}
    requestString = 'http://localhost:5000/api/access/users/' + username
    http_get_result = requests.delete(requestString, headers=headers)
    print(http_get_result)
    return http_get_result.status_code

############################ connections handling    ************************
@uamethod
def con(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'connect',
            'port': '',
            'baudrate': 115200,
            'printerProfile': '',
            'save': True,
            'autoconnect' : True}
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code
@uamethod
def discon(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'disconnect'}
    requestString = 'http://localhost:5000/api/connection'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

######################### general information

@uamethod
def log_in(parent, api_key, user, passw):
    headers = {'X-Api-Key' : api_key.Value}
    data = { 'user' : user,
             'pass' : passw,
             'remember' : True}
    requestString = 'http://localhost:5000/api/login'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code
@uamethod
def Log_out(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    requestString = 'http://localhost:5000/api/logout'
    http_get_result = requests.post(requestString, headers=headers)
    print(http_get_result)
    return http_get_result.status_code

######################### general information

#########################job Operations

@uamethod
def start_job(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'start'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

@uamethod
def cancel_job(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'cancel'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code
@uamethod
def restart_job(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'restart'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

@uamethod
def resume_job(parent, api_key):
    headers = {'X-Api-Key' :api_key.Value}
    data = {'command' : 'pause', 'action' : 'resume'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

@uamethod
def pause_job(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'pause', 'action' : 'pause'}
    requestString = 'http://localhost:5000/api/job'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

#########################job Operations

#########################printer Operatioins

@uamethod
def home_head(parent, api_key):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'home', 'axes' : ['x', 'y']}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code
@uamethod
def move_head(parent, api_key, x, y, z):
    headers = {'X-Api-Key' : api_key.Value}
    data = {'command' : 'jog',
            'x' : x,
            'y' : y,
            'z' : z}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code
@uamethod
def set_feedrate_head(parent, api_key, n):
    data = {'command' : 'feedrate', 'factor' : n}
    headers = {'X-Api-Key' : api_key}
    requestString = 'http://localhost:5000/api/printhead'
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

#####################################################################
@uamethod
def upload_file(parent, api_key, url, name):
    print("start download")

    file_name = wget.download(str(url))
    file_data = {'file': open(file_name, 'rb'), 'filename': str(name)}

    print("download finished")
    print('file_name')
    print(file_data)

   # fle={'file': open('/c/newfile.gcode', 'rb'), 'filename': str(name)}

    os.remove(file_name)
    print('file removed')

    payload = {"select":"ture", "print":"false"}

    headers = {'X-Api-Key' : api_key.Value}
    requestString = 'http://localhost:5000/api/files/local'
    http_get_result = requests.post(requestString, files=file_data, data=payload, headers=headers)
    print(http_get_result)
    return http_get_result.status_code


@uamethod
def select_file(parent, api_key, filename, location, start):
    data = {'command':'select', 'print': start}
    headers = {'X-Api-Key' : api_key.Value}
    requestString = 'http://localhost:5000/api/files/' + location + '/'+filename
    http_get_result = requests.post(requestString, headers=headers, json=data)
    print(http_get_result)
    return http_get_result.status_code

@uamethod
def delete_file(parent, api_key, location, path):
    headers = {'X-Api-Key' : api_key.Value}
    requestString = 'http://localhost:5000/api/files/' + location + '/'+path
    http_get_result = requests.delete(requestString, headers=headers)
    print(http_get_result)
    return http_get_result.status_code