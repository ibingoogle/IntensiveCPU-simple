#!/bin/python
from __future__ import print_function
import Pyro4
import socket
import os
import sys
from threading import Thread
import threading
import re
import json
import xmltodict

mutex = threading.Lock() 

class SocketHttp(Thread):

    def __init__(self, monitor_master):
        Thread.__init__(self)
        self.monitor_master = monitor_master
        self.write_pid()
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

    def write_pid(self):
        process_id = os.getpid()
        pid_file = sys.path[0]
        try:
            file = open(pid_file + "/httpserver_pid", "w")
            file.write(str(process_id))
        except (IOError,OSError) as error:
            print("error during cluster_file loading %s", error)
            file.close()

    def start(self):
        Thread.start(self)

    def run(self):
        index=1
        #infinite loop
        while True:
            index = index + 1
            self.post_content = self.monitor_master.get_monitor()
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


@Pyro4.expose
class Master_Monitor(object):

    def __init__(self, pid_file):
        self.slaves=[]
        self.monitor={}
        self.cluster_file = pid_file + "/cluster.txt"
        self.load_cluster()

    def add_slave(self, slave):
        if slave in self.slaves:
            return
        self.slaves.append(slave)
        self.monitor[slave]={}

    def load_cluster(self):
        try:
            file = open(self.cluster_file, "r")
            lines = file.readlines()
            for line in lines:
                ip = line.split("\n")[0]
                self.monitor[ip] = 0
        except (IOError,OSError) as error:
            print("error during cluster_file loading %s", error)

    def update_monitor(self, slave, result):
        mutex.acquire()
        self.monitor[slave] = result
        mutex.release()

    def get_monitor(self):
        return self.monitor

    def print_slave(self):
        for slave in self.slaves:
            print("slave = ", slave)

    def print_monitor(self, slave=None):
        if slave:
            print(self.monitor[slave])
            return
        print("~~~~~~~~~~~~~~~~")
        print(self.monitor)
        return


class RPCThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)

    def start(self):
        Thread.start(self)

    def run(self):
        daemon = Pyro4.Daemon(host='192.168.2.30')
        ns     = Pyro4.locateNS()
        uri    = daemon.register(Master_Monitor)
        ns.register("Master_Monitor", uri)
        daemon.requestLoop()

def main(master_monitor):
 
    daemon = Pyro4.Daemon(host='192.168.2.30')
    ns     = Pyro4.locateNS()
    uri    = daemon.register(master_monitor)
    ns.register("Master_Monitor", uri)
    daemon.requestLoop()


if __name__=="__main__":
    process_id = os.getpid()
    pid_file = sys.path[0]
    try:
        file = open(pid_file + "/NetworkMonitor_pid", "w")
        file.write(str(process_id))
    except (IOError,OSError) as error:
        print("error during cluster_file loading %s", error)
    file.close()
    master_monitor = Master_Monitor(pid_file)
    socket_http = SocketHttp(master_monitor)
    socket_http.start()
    main(master_monitor)
    print("!!!!!!!!!!!!!!")
