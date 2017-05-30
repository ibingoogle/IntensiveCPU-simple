#!/bin/python
from threading import Thread
import time
import subprocess
import sys
import Pyro4
import socket
import os


class NetStat(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.is_netstat = True
        self.command = "netstat -t"
        self.content = []
        self.interval = 0.5

    def start(self):
        self.is_netstat = True
        Thread.start(self)

    def run(self):
        while self.is_netstat == True:
            val = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE)
            val.wait()
            self.content =  val.stdout.readlines()
            time.sleep(self.interval)


class Monitor(Thread):

    def __init__(self, pid_file):
        Thread.__init__(self)
        self.content = []
        self.interval = 1
        self.is_monitor = True
        self.netstat = NetStat()
        self.cluster_file = pid_file + "/cluster.txt"
        # print(self.cluster_file)
        self.cluster = []
        self.flow_current = []
        self.flow_send = {}
        self.flow_receive = {}
        self.hostname = socket.getfqdn(socket.gethostname())
        self.ip = socket.gethostbyname(self.hostname)

    def start(self):
        self.is_monitor = True
        self.load_cluster()
        self.netstat.start()
        Thread.start(self)

    def run(self):
        master_monitor = self.get_proxy()
        while self.is_monitor == True:
            self.content =  self.netstat.content
            time.sleep(self.interval)
            self.load_flow()
            master_monitor.update_monitor(self.hostname, self.flow_send)
            #master_monitor.print_monitor()

    def register(self):
        master_monitor = self.get_proxy()
        master_monitor.add_slave(self.hostname)
        master_monitor.print_slave()
        master_monitor.print_monitor()

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
        #print(self.content)
        del self.flow_current[:]
        self.reset_flow_send_receive()
        for line in self.content:
            #flow = line.split("\n")[0]
            #print(line)
            str_line = str(line, encoding="utf-8")
            #print(str_line)
            flow = str_line.split("\n")[0]
            flow_splited = flow.split()
            #print len(flow_splited
            sub_flow = []
            if len(flow_splited) == 6:
            	for split in flow_splited:
                    sub_flow.append(split)
                    self.flow_current.append(sub_flow)
                    #print self.flow_current
        for sub_flow in self.flow_current:
            ForeignAddressIp = sub_flow[4].split(":")[0]
            receive = sub_flow[1]
            send = sub_flow[2]
            if self.belong_cluster(ForeignAddressIp) == True:
                current_receive = self.flow_receive[ForeignAddressIp]
                current_send    = self.flow_send[ForeignAddressIp]
                self.flow_receive[ForeignAddressIp] = current_receive + int(receive)
                self.flow_send[ForeignAddressIp]    = current_send    + int(send)
                self.print_flow_send()

    def get_proxy(self):
        master_monitor = Pyro4.Proxy("PYRONAME:Master_Monitor")
        return master_monitor


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


def main():
    process_id = os.getpid()
    pid_file = sys.path[0]
    try:
        file = open(pid_file + "/netstat_pid", "w")
        file.write(str(process_id))
    except (IOError,OSError) as error:
        print("error during cluster_file loading %s", error)
    file.close()

    monitor = Monitor(pid_file)
    monitor.register()
    monitor.start()

if __name__=="__main__":
    main()
