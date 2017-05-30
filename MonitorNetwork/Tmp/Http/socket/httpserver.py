import socket
import re
import json
import xmltodict
import sys
import os

def to_json(Dict):
    jdata = json.dumps(Dict)
    return jdata

def to_xml(Dict):
    root_Dict = {}
    root_Dict['root'] = Dict
    convertedXml = xmltodict.unparse(root_Dict);
    return convertedXml

# load conf file
cur_path = sys.path[0]
try:
    file = open(cur_path + "/conf", "r")
    HOST = file.readline().strip("\n")
    PORT = int(file.readline().strip("\n"))
    form = file.readline().split("=")[1].strip("\n")
except (IOError,OSError) as error:
    print("error during conf loading %s", error)
    file.close()

#write pid file
process_id = os.getpid()
pid_file = sys.path[0]
try:
    file = open(pid_file + "/httpserver_pid", "w")
    file.write(str(process_id))
except (IOError,OSError) as error:
    print("error during cluster_file loading %s", error)
    file.close()

# get defaule values
post_content ={'user':'swang', 'a':'1','b':'2'}
if form == "json":
    converted_values = to_json(post_content)
else:
    converted_values = to_xml(post_content)
content = converted_values

#Configure socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((HOST, PORT))
sock.listen(1)

index=1

#infinite loop
while True:
    index = index + 1
    post_content['user'] = str(index)
    # maximum number of requests waiting
    conn, addr = sock.accept()
    request = conn.recv(1024)
    request_str = str(request, encoding = "utf-8")
    method = request_str.split(' ')[0]

    print ('Connect by: ', addr)
    print ('Request is:\n', request)


    if form == "json":
        converted_values = to_json(post_content)
    else:
        converted_values = to_xml(post_content)
    content = converted_values


    print("content = ", content)
    conn.sendall(bytes(content, encoding='utf-8'))
    
    #close connection
    conn.close()



