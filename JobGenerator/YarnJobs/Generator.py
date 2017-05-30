#!/bin/python
import time
import ConfUtils
import math
import random
import JobRecorder

class Generator:

    ## a generator can only sumbit job into one queue
    def __init__(self,prefix,conf,queueMonitor):
        if prefix is not None:   # an affix that is added in front of thr word including Order, Poission and Capacity
            self.PREFIX_NAME = "generator." + prefix
        else:
            print "prefix is none"

        self.conf           = conf

        if conf.get(self.PREFIX_NAME + ".queue") is None: # we can specify which queue we submit the job into
            self.queue = "default" # if we do not specify, use the default queue
        else:
            self.queue = conf.get(self.PREFIX_NAME + ".queue")[0]

        self.queueMonitor   = queueMonitor

        self.job_types      = []  ## different job types, can be hadoop, spark, sparksql or hibench.
        self.job_types      += conf.get(self.PREFIX_NAME + ".jobs")
        
        self.job_maker_sets = {} ## corresponding to the job_types, for each type we have a jobmaker

        self.job_count      = 0  ## count the number of this jobs

        self.index          = -1 ## record the index of current jobs(hadoop, spark, sparksql)

        ## TODO Reflection
        for job in self.job_types:
            if job == "hadoop":
                job_maker = JobRecorder.HadoopMakeJob(conf,self.queue)
            elif job == "spark":
                job_maker = JobRecorder.SparkMakeJob(conf,self.queue)
            elif job == "sparksql":
                job_maker = JobRecorder.SparkSQLMakeJob(conf,self.queue)
            elif job == "hibench":
                job_maker = JobRecorder.HiBenchMakeJob(conf,self.queue)
            else:
                print "error: job type not exits"
            self.job_maker_sets[job] = job_maker

        ##must have at least 1 job type
        assert(len(self.job_types) > 0)

        ##job.ratios could be null
        jobratios = conf.get(self.PREFIX_NAME + ".jobs.ratios")
        if jobratios is None: # equal share if we do not configure it
            self.job_ratios = [1 for i in range(len(self.job_types))]
        else:
            self.job_ratios = map(lambda x:float(x), conf.get(self.PREFIX_NAME + ".jobs.ratios"))

        ## read in parameter which we want to update during execution
        self.parameter_service = ConfUtils.ParameterService(conf=self.conf, PREFIX_NAME=self.PREFIX_NAME)
        ## last time to call generate_request
        self.last           = 0
        pass









##### generate request in order
class OrderGenerator(Generator):

    def __init__(self,prefix,conf,queueMonitor):
        Generator.__init__(self,prefix,conf,queueMonitor)
        self.current_job = None
        self.count = 0
        self.index = 0
        self.exist = False

        order = self.conf.get(self.PREFIX_NAME + ".order")
        if order[0] is None:
            self.order = False
            return
        if order[0] == "true":
            self.order = True
        else:
            self.order = False

        round = self.conf.get(self.PREFIX_NAME + ".round")[0]
        if round is None:
            self.round = 1
        else:
            self.round = int(round)

        range = self.conf.get(self.PREFIX_NAME + ".range")[0]
        if range is None:
            self.range = 1
        else:
            self.range = int(range)

        print "self.order = ", self.order
        print "self.round = ", self.round
        print "self.range = ", self.range


##### generate request in Poisson distribution
class PoissonGenerator(Generator):

    def __init__(self,prefix,conf,queueMonitor):
        Generator.__init__(self,prefix,conf,queueMonitor)
        ## how long(s) we need to check if we need to submit a job
        self.interval = self.parameter_service.get_parameter("interval")
        ## means for poisson distribution
        self.mean     = self.parameter_service.get_parameter("mean")
    
        print "self.interval = ", self.interval
        print "self.mean = ", self.mean

    def _update_(self):
        self.interval = self.parameter_service.get_parameter("interval")
        self.mean     = self.parameter_service.get_parameter("mean")





##### generater request in to match the capacity that user set
class CapacityGenerator(Generator):

    def __init__(self,prefix,conf,queueMonitor):
        Generator.__init__(self,prefix,conf,queueMonitor)
        ## we wait 10s to make our new submission effectively occupy the cluster resource
        self.interval       = 10
        self.usedCapacity   = self.parameter_service.get_parameter("usedCapacity")

    def _update_(self):
        self.usedCapacity   = self.parameter_service.get_parameter("usedCapacity")
        
