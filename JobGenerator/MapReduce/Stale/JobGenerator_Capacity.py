from random import Random
import json
import os
import commands
import subprocess
import time

def random_str(randomlength):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

class InputData:
    inputdata_base = ""
    inputdata = ""

    def __init__(self):
        self.inputdata_base = "/hadoop/benchmark/wordcount/inputdata/size/"
        self.inputdata = self.inputdata_base

    def get_inputdata(self,size,number):
        if size == "5m" or size == "10m" or size == "20m" or size == "40m" or size == "60m" or size == "80m" or size == "100m" or size == "120m":
            self.inputdata = self.inputdata_base + size
        else:
            print "error file size"
            return 0
        if number <= 10 and number >= 1:
            self.inputdata = self.inputdata + "/[0-" + str(number-1) + "].txt"
            print "self.inputdata: " + self.inputdata
            return self.inputdata
        else:
            print "error file number"
            return 0

class OutputData:
    outputdata_base = ""
    outputdata = ""
    output_randomlength = 6

    def __init__(self):
        self.outputdata_base = "/hadoop/benchmark/wordcount/outputdata/size/"
        self.outputdata = self.outputdata_base
        self.output_randomlength = 6

    def get_outputdata(self,size):
        if size == "5m" or size == "10m" or size == "20m" or size == "40m" or size == "60m" or size == "80m" or size == "100m" or size == "120m":
            randomstr = random_str(self.output_randomlength)
            self.outputdata = self.outputdata_base + size + "/output_" + randomstr
            print "self.outputdata" + self.outputdata
            return self.outputdata
        else:
            print "error size"
            return 0

    def delete_outputdata(self):
        command = "hdfs dfs -rm -r " + self.outputdata
        print "command: " + command
        val = subprocess.call(command,shell=True)

if __name__ == "__main__":
    Version = "2.7.2"
    size = "20m"
    mapsnumber = 4
    inputData = InputData()
    inputPath = inputData.get_inputdata(size,mapsnumber)
    size2 = "5m"
    mapsnumber2 = 5
    inputData2 = InputData()
    inputPath2 = inputData2.get_inputdata(size2,mapsnumber2)


    outputData = OutputData()
    outputPath = outputData.get_outputdata(size)
    outputData2 = OutputData()
    outputPath2 = outputData2.get_outputdata(size2)
    
    queuename = "-Dmapred.job.queue.name=queue1"
    queuename2 = "-Dmapred.job.queue.name=queue2"

    benchmark = "wordcountgeneratereduceless"
    command_base = "hadoop jar /opt/modules/hadoop-" + Version + "-modified/hadoop-" + Version + "/share/hadoop/mapreduce/hadoop-mapreduce-examples-" + Version + ".jar " + benchmark + " "
    command1 = command_base + queuename + " " + inputPath + " " + outputPath
    command2 = command_base + queuename2 + " " + inputPath2 + " " + outputPath2
    print command2
  
    #val1 = subprocess.Popen(command1,shell=True)
    #time.sleep(3)
    val2 = subprocess.Popen(command2,shell=True)
    #val1.wait()
    val2.wait()

    #outputData.delete_outputdata()
    outputData2.delete_outputdata()
    print "The end"

