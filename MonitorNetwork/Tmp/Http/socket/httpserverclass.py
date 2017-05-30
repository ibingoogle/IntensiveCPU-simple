import socket
import re
import json
import xmltodict
import sys
import os
from threading import Thread



class SocketHttp(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.host = ""
        self.port = 80
        self.conf = "/conf"
        self.form = "xml"
        self.post_content = {'user':'swang', 'a':'1','b':'2'}
        self.load_conf()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def start(self):
        Thread.start(self)

    def run(self):
        index=1
        #infinite loop
        while True:
            index = index + 1
            self.post_content['user'] = str(index)
            # maximum number of requests waiting
            conn, addr = self.sock.accept()
            request = conn.recv(1024)
            request_str = str(request, encoding = "utf-8")

            print ('Connect by: ', addr)
            print ('Request is:\n', request)
             
            content = self.convert_content(self.post_content)
            print("content = ", content)
            conn.sendall(bytes(content, encoding='utf-8'))
            #close connection
            conn.close()

    def load_conf(self):
        cur_path = sys.path[0]
        try:
            file = open(cur_path + self.conf, "r")
            self.host = file.readline().strip("\n")
            self.port = int(file.readline().strip("\n"))
            self.form = file.readline().split("=")[1].strip("\n")
        except (IOError,OSError) as error:
            print("error during conf loading %s", error)
            file.close()

    def convert_content(self,post_content):
        if self.form == "json":
            converted_values = self.to_json(post_content)
            return converted_values
        converted_values = self.to_xml(post_content)
        return converted_values


    def to_json(self,Dict):
        jdata = json.dumps(Dict)
        return jdata

    def to_xml(self,Dict):
        root_Dict = {}
        root_Dict['root'] = Dict
        convertedXml = xmltodict.unparse(root_Dict);
        return convertedXml


if __name__ =="__main__":
    #write pid file
    process_id = os.getpid()
    pid_file = sys.path[0]
    try:
        file = open(pid_file + "/httpserver_pid", "w")
        file.write(str(process_id))
    except (IOError,OSError) as error:
        print("error during cluster_file loading %s", error)
        file.close()

    socket_http = SocketHttp()
    socket_http.start()
    print("!!!!!!!!!!!!!!")
    

