#!/bin/python
from threading import Thread
import time
import subprocess
import sys
import Pyro4
import socket
import os

class Iftop(Thread):

    def __init__(self, pid_file):
        Thread.__init__(self)
        self.is_iftop = True
        self.interval = 1
        self.command = "sudo iftop -t -s " + str(self.interval) + " -B"
        self.content = []
        self.cluster_file = pid_file + "/cluster.txt"
        self.cluster = []
        self.flow_send = {}
        self.flow_receive = {}
        self.hostname = socket.getfqdn(socket.gethostname())
        self.ip = socket.gethostbyname(self.hostname)

    def register(self):
        master_monitor = self.get_proxy()
        master_monitor.add_slave(self.hostname)
        master_monitor.print_slave()
        master_monitor.print_monitor()
        
    def get_proxy(self):
        master_monitor = Pyro4.Proxy("PYRONAME:Master_Monitor")
        return master_monitor


    def start(self):
        self.is_iftop = True
        self.load_cluster()
        Thread.start(self)

    def run(self):
        i = 0
        master_monitor = self.get_proxy()
        while self.is_iftop == True:
            val = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE)
            val.wait()
            return_content =  val.stdout.readlines()
            self.content = []
            Begin = False
            End   = False
            for line in return_content:
                if End == True:
                    break
                str_line = str(line, encoding="utf-8").split("\n")[0]
                if "---" in str_line:
                    if Begin == True:
                        End = True
                        Begin = False
                    else:
                        Begin = True
                    continue
                if Begin == True:
                    self.content.append(str_line)
                    #print(str_line)
            self.load_flow()
            master_monitor.update_monitor(self.hostname, self.flow_send)
            master_monitor.print_monitor()
            print(i)
            i = i + 1


    def load_cluster(self):
        del self.cluster[:]
        self.flow_send.clear()
        self.flow_receive.clear()
        try:
            file = open(self.cluster_file, "r")
            lines = file.readlines()
            for line in lines:
                ip = line.split("\n")[0]
                self.cluster.append(ip)
                self.flow_send[ip] = 0
                self.flow_receive[ip] = 0
                #print self.cluster
        except (IOError,OSError) as error:
            print("error during cluster_file loading %s", error)
            return False
        return True

    def load_flow(self):
        self.reset_flow_send_receive()
        line_flag = -1
        prev_line = ""
        for line in self.content:
            line_flag = line_flag + 1
            if line_flag%2 == 0:
                prev_line = line
                continue
            #print(prev_line)
            #print(line)
            line_splited = line.split()
            #print (len(line_splited))
            ForeignAddressIp = line_splited[0]
            if self.belong_cluster(ForeignAddressIp) == True:
                Send = prev_line.split()[3]
                Recv = line_splited[2]
                format_Send = self.format_KB(Send)*2
                format_Recv = self.format_KB(Recv)*2
                self.flow_receive[ForeignAddressIp] = format_Recv
                self.flow_send[ForeignAddressIp]    = format_Send
        #self.print_flow_send()
        #self.print_flow_receive()

    def belong_cluster(self,ForeignAddressIp):
        #print ForeignAddressIp
        if ForeignAddressIp in self.cluster:
            return True
        return False

    def print_flow_send(self):
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        for key in self.flow_send:
            print("ip: ", key)
            print("send: ", self.flow_send[key])

    def print_flow_receive(self):
        print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        for key in self.flow_receive:
            print("ip: ", key)
            print("receive: ", self.flow_receive[key])

    def reset_flow_send_receive(self):
        for key in self.flow_send:
            self.flow_send[key] = 0
        for key in self.flow_receive:
            self.flow_receive[key] = 0

    def format_KB(self, origin):
        if "MB" in origin:
            str_num = origin.split("MB")[0]
            return float(str_num)*1024
        elif "KB" in origin:
            str_num = origin.split("KB")[0]
            return float(str_num)
        elif "B" in origin:
            str_num = origin.split("B")[0]
            return float(str_num)/1024

def main():
    process_id = os.getpid()
    pid_file = sys.path[0]
    try:
        file = open(pid_file + "/iftop_pid", "w")
        file.write(str(process_id))
    except (IOError,OSError) as error:
        print("error during cluster_file loading %s", error)
    file.close()

    iftop = Iftop(pid_file)
    # iftop.register()
    iftop.start()

if __name__=="__main__":
    main()
