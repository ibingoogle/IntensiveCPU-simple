#!/bin/python






PROGRESS ="progress"
CONTAINER="runningContainers"
MB       ="allocatedMB"
VCORE    ="allocatedVCores"
STATE    ="state"
FINISH   ="finishedTime"
START    ="startedTime"
ELAPSE   ="elapsedTime"

class JobInfo:

    def __init__(self,job_id):
        self.job_id      = job_id
        self.job_name    = None
        self.start_time  = 0
        self.finish_time = 0
        self.run_time    = 0 ## the difference between elapse_time and start_time
        self.state       = None # come from dict_read[STATE], can be ACCEPTED, SUBMITTED, RUNNNING and FINISHED
        self.finish      = False # based on dict_read[STATE]
        self.statics     ={}# statistics about progress, runnning containers, allocatedMB, allocatedVCores

    def monitor(self,dict_read):
        elapse_time = int(dict_read[ELAPSE])
        ##record start time
        if self.start_time == 0:
            self.start_time = int(dict_read[START])

        ##record run_time if applicable
        if (self.state == "ACCEPTED" or self.state =="SUBMITTED") and (dict_read[STATE]=="RUNNING"):
            self.run_time = self.start_time + elapse_time 
        ##record state
        self.state = dict_read[STATE]

        ##record progress with elapse time
        if self.statics.get(PROGRESS) is None:
            self.statics[PROGRESS] = {}
        self.statics[PROGRESS][elapse_time]=float(dict_read[PROGRESS])
        ##record container with elapse time
        if self.statics.get(CONTAINER) is None:
            self.statics[CONTAINER] = {}
        self.statics[CONTAINER][elapse_time]=int(dict_read[CONTAINER])
        ##record memory with elapse time
        if self.statics.get(MB) is None:
            self.statics[MB] = {}
        self.statics[MB][elapse_time]=int(dict_read[MB])
        ##record cores with elapse time
        if self.statics.get(VCORE) is None:
            self.statics[VCORE] = {}
        self.statics[VCORE][elapse_time]=int(dict_read[VCORE])

        ##record finish time
        if dict_read[STATE] == "FINISHED":
            self.finish = True
            self.finish_time=int(dict_read[FINISH])
        pass

