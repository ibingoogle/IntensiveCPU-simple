#!/bin/python


import os
import subprocess
import time
import random
import threading
import ConfUtils







PROGRESS  = "progress"
CONTAINER = "runningContainers"
MB        = "allocatedMB"
VCORE     = "allocatedVCores"
STATE     = "state"
FINISH    = "finishedTime"
START     = "startedTime"
ELAPSE    = "elapsedTime"




class MakeJob: ## corresponding to different types of jobs, the following is common info to make different type jobs

    PREFIX_NAME = None


    def __init__(self,conf,queue):
        self.conf       = conf
        self.job_conf   = {} ## store the detail configuration of different benchmark(kind of jobs)
        self.job_home   = None
        self.job_user   = conf.get("user")[0]  ## the user like admin
        self.queue      = queue
       
        ## get benchmark info
        self.jobs       = []  ## the specific benchmark like wordcount and sort
        if conf.get(self.PREFIX_NAME) is None:
            raise Exception("jobs can not be null")

        self.jobs      += conf.get(self.PREFIX_NAME) ## the prefix_name can be "hadoop.jobs","spark.jobs"......

        ## get ratios between benchmarks info
        if conf.get(self.PREFIX_NAME + ".ratios") is None:
            ## equal share : [1,1,1,1,....]
            self.ratios = [1 for i in range(len(self.jobs))]
        else:
            self.ratios = map(lambda x:float(x), conf.get(self.PREFIX_NAME + ".ratios")) # may be [1,2]
        ## Verify the ratios configuration, we should terminate here is we have exception
        if len(self.jobs) != len(self.ratios):
            raise Exception("jobs and ratios miss match")

        ## get the detail information for each benchmark
        for job in self.jobs:
            # use dictionary to store details information
            self.job_conf[job] = {} 
            ##TODO we can do some check here, first we get the jars
            if conf.get(self.PREFIX_NAME + "." + job + ".jars") is None:
                self.job_conf[job]["jars"] = ""
            else:
                self.job_conf[job]["jars"] = conf.get(self.PREFIX_NAME + "." + job + ".jars")[0]
            ## we get the input_path
            self.job_conf[job]["inputs"] = [] # use array, we may have several inputs 
            if conf.get(self.PREFIX_NAME + "." + job + '.inputs') is None:
                self.job_conf[job]["inputs"] = ""
            else:
                self.job_conf[job]["inputs"] += conf.get(self.PREFIX_NAME + "." + job + '.inputs')
            ## we get the output_path
            if conf.get(self.PREFIX_NAME + "." + job + ".output") is None:
                self.job_conf[job]["output"] = None
            else:
                self.job_conf[job]["output"] = conf.get(self.PREFIX_NAME + "." + job + ".output")[0]
            ## we get the parameters
            ## hadoop.jobs.wordcount.parameters should use hadoop.jobs.parameters if it is null
            parameters = []
            if conf.get(self.PREFIX_NAME + "." + job + ".parameters") is not None:
                parameters += conf.get(self.PREFIX_NAME + "." + job + ".parameters")
            elif conf.get(self.PREFIX_NAME + ".parameters") is not None:
                parameters += conf.get(self.PREFIX_NAME + ".parameters")
            else:
                pass
            self.job_conf[job]["parameters"] = parameters
            ## we get the keyvalues
            ## hadoop.jobs.wordcount.keyvalues should use hadoop.jobs.keyvalues if it is null
            keyvalues = []
            if conf.get(self.PREFIX_NAME + "." + job + ".keyvalues") is not None:
                keyvalues += conf.get(self.PREFIX_NAME + "." + job + ".keyvalues")
            elif conf.get(self.PREFIX_NAME + ".keyvalues") is not None:
                keyvalues += conf.get(self.PREFIX_NAME + ".keyvalues")
            else:
                pass
            ## convert keyvalues to key_values
            key_values = {}        
            for keyvalue in keyvalues:
                key   = keyvalue.split(":")[0].strip()
                value = keyvalue.split(":")[1].strip()
                key_values[key] = value
            self.job_conf[job]["keyvalues"] = key_values


class HadoopMakeJob(MakeJob): # derived from MakeJob, designed for Hadoop job
    
    PREFIX_NAME = "hadoop.jobs"

    def __init__(self,conf,queue):
        print "hadoopMakeJob"
        MakeJob.__init__(self,conf,queue)
        self.job_home = self.conf.get("hadoop.home")[0]



class SparkMakeJob(MakeJob):
    
    PREFIX_NAME = "spark.jobs"

    def __init__(self,conf,queue):
        print "SparkMakeJob"
        MakeJob.__init__(self,conf,queue)
        self.job_home = self.conf.get("spark.home")[0]


class SparkSQLMakeJob(MakeJob):

    PREFIX_NAME = "sparksql.jobs"

    def __init__(self,conf,queue):
        print "SparkSQLMakeJob"
        MakeJob.__init__(self,conf,queue)
        self.job_home = self.conf.get("spark.home")[0]


class HiBenchMakeJob(MakeJob):

    PREFIX_NAME = "hibench.jobs"

    def __init__(self,conf,queue):
        print "HiBenchMakeJob"
        MakeJob.__init__(self,conf,queue)
        self.job_home = self.conf.get("hibench.home")[0]
        ## hibench can generate different types of jobs, so we need to know the detail
        types = self.conf.get("hibench.jobs.types")
        if types is None: ## we use mapreduce as default job type
            self.job_types = ["mapreduce" for i in range(len(self.jobs))]
        else:
            self.job_types = types

