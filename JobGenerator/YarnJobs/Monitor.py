import time
import ConfUtils
import Scheduler
# use Threading mode to create thread, derived from the class of threading.Thread, then override the two functions: __init__() and run()
from threading import Thread 
from JobInfo import JobInfo


##for capacity scheduler


ABCP    = "absoluteCapacity"
ABMXCP  = "absoluteMaxCapacity"
## the following parameters dynamically change when there are applications running in cluster
## So we record their value at each time interval
ABUSE   = "absoluteUsedCapacity"
NMAPP   = "numApplications"
NMACAPP = "numActiveApplications"
NMPEAPP = "numPendingApplications"
NMCON   = "numContainers"
USECP   = "usedCapacity"


##for FIFO scheduler

USENOCAP = "usedNodeCapacity"
AVANOCAP = "availNodeCapacity"
TOTALCAP = "totalNodeCapacity"

class Monitor(Thread):  #derived from the class of threading.Thread

    def __init__(self,conf): #rewrite the __init__ function
        Thread.__init__(self) # the original __init__ function in threading.Thread function
        self.conf = conf # get the configuration
        past = 0.8
        print "Monitor.conf: ", conf.confs
        self.start_time = str(int(time.time()*1000*past))
        print "self.start_time: ", self.start_time
        # get the url of cluster's scheduler information
        self.scheduler_url = conf.get("hadoop.url")[0]+"/ws/v1/cluster/scheduler"
        # get the url of job's information
        self.job_url = conf.get("hadoop.url")[0]+"/ws/v1/cluster/apps?startedTimeBegin="+self.start_time
        print "self.scheduler_url: ", self.scheduler_url
        print "self.job_url: ", self.job_url

        # mapping from the queue to finished jobs
        ##use dictionary to store the job's information
        self.job_infos = {} #first level is queue, second level is job_id, second level value is jobInfo
        ##record running job id using the set() data structure
        self.running = set() # the element is job_id
        ##record finished job id using the set() data structure
        self.finish  = set() # the element is job_id
        ##if the working thread is running, default to be false
        self.is_running = False
        ##record the queue info using dictionary
        self.queue_info = {} # first level is queue_name, second level is parameter, third is timestampe
        ##record the submit info using dictionary
        self.submit_info = {}


    def start(self):   # override the start() function serived from Thread class
        self.is_running = True  # make sure that this thread can keep running
        Thread.start(self)   # including the original start() function in Thread class
    
    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running: # keep monitoring
            ## monitor the information of jobs
            self.monitor_jobs()
            ## monitor the scheduling and queue information in the cluster
            self.monitor_queue()
            ## sleep for 10 seconds
            time.sleep(3)

    ## return running job_dicts
    def get_job_dicts(self):
        dict_read = ConfUtils.read_json_url(self.job_url)
        if dict_read is None: ## the job_url is wrong
            print "error dict_read"
            return None
        if dict_read["apps"] is None: # no job has been submitted yet
            return None
        return dict_read["apps"]["app"]


    def monitor_jobs(self):
        job_dicts = self.get_job_dicts()
        if job_dicts is None:
            print "there is no job available"
            return
        print "there are jobs available"

        for job_dict in job_dicts:
            id    = job_dict["id"]
            queue = job_dict["queue"]
            ## we ignore the finished job, just continue
            if id in self.finish:
                continue
            ## for jobs not finished yet, but it has been marked as running job
            elif id in self.running:
                job = self.job_infos[queue].get(id) # get the running job base on id
                job.monitor(job_dict) ## monitor job based on current job_dict, update information based on time
                if job.finish is True:  ## decide whether the job has finished
                    self.running.remove(id)
                    self.finish.add(id)
            ## it is a new job
            else:
                ## create the queue if we have not added jobs into it
                if self.job_infos.get(queue) is None:
                    self.job_infos[queue] = {}
                self.job_infos[queue][id] = JobInfo(id) # the value in second level is the instance of class JobInfo
                self.running.add(id)
                # monitor the job first time
                self.job_infos[queue][id].monitor(job_dict) # pass the job info through job_dict
        pass


    def monitor_queue(self):
        pass


    @staticmethod
    def get_scheduler_type(conf):
        # get the url of cluster's scheduler based on cluster's configuration
        scheduler_url = conf.get("hadoop.url")[0] + "/ws/v1/cluster/scheduler"
        dict_read = ConfUtils.read_json_url(scheduler_url)
        scheduler_type = dict_read["scheduler"]["schedulerInfo"]["type"]
        print "scheduler_type: ", scheduler_type
        return scheduler_type





class FifoQueueMonitor(Monitor): ## derived from the Monitor class

    def __init__(self,conf):
        print "This initialization is for FifoScheduler"
        Monitor.__init__(self,conf)   ## initialize the Monitor class first

    def monitor_queue(self): # begin to monitor queue
        ## read the cluster's scheduling information
        dict_read = ConfUtils.read_json_url(self.scheduler_url)
        # get the info of scheduler's type
        scheduler_type = dict_read["scheduler"]["schedulerInfo"]["type"]
        if scheduler_type != "fifoScheduler":
            ##TODO
            print "only support fifo scheduler"
            return
        # get all other informations in FifoScheduler
        root_queue = dict_read["scheduler"]["schedulerInfo"]
        self.queue_info[USENOCAP] = root_queue[USENOCAP]
        self.queue_info[AVANOCAP] = root_queue[AVANOCAP]
        self.queue_info[TOTALCAP] = root_queue[TOTALCAP]
        print "self.queue_info[USENOCAP]: ", root_queue[USENOCAP]
        print "self.queue_info[AVANOCAP]: " , root_queue[AVANOCAP]
        print "self.queue_info[TOTALCAP]: ",  root_queue[TOTALCAP]



class CapacityQueueMonitor(Monitor): ## derived from the Monitor class

    def __init__(self,conf):
        print "This initialization is for CapacityScheduler"
        Monitor.__init__(self,conf)
        ##absolute capacity
        self.abcp = 0
        ##absolute max capacity
        self.abmcp = 0

    ##current we only support capacity scheduler
    def monitor_queue(self): # begin to monitor queue1
        dict_read = ConfUtils.read_json_url(self.scheduler_url)
        scheduler_type = dict_read["scheduler"]["schedulerInfo"]["type"]
        if scheduler_type != "capacityScheduler":
            ##TODO
            print "only support capacity scheduler"
            return
        # get all the information about this capacity scheduler
        root_queue = dict_read["scheduler"]["schedulerInfo"]
        # print "root_queue: ", root_queue
        # store all the information using traverser_update_queue() function
        self.traverse_update_queue(root_queue)
        return

    
    def traverse_update_queue(self,root_queue): # We traverse the cluster's scheduler info and update them
        child_queues = root_queue.get("queues")
        ## we reach the leaf queue
        if child_queues is None:
            ## we find the leaf queue and update queue
            name = root_queue["queueName"]
            self.update_queue(name,root_queue)
        ## WE TRAVERSE its children
        else:
            for queue in child_queues["queue"]:
                self.traverse_update_queue(queue)

        
    def update_queue(self,queue_name,this_queue):
        ELAPSE = int(time.time() - Scheduler.START_TIME)
        ## insert queue into queue_info when it does not exist (first time update)
        if self.queue_info.get(queue_name) is None:
            self.queue_info[queue_name] = {} ## insert new queue and initialziation

        self.queue_info[queue_name][ABCP] = float(this_queue[ABCP])
        self.queue_info[queue_name][ABMXCP] = float(this_queue[ABMXCP])

        if self.queue_info[queue_name].get(ABUSE) is None:
            self.queue_info[queue_name][ABUSE] = {}
        self.queue_info[queue_name][ABUSE][ELAPSE] = float(this_queue[ABUSE])
        
        if self.queue_info[queue_name].get(NMAPP) is None:
	        self.queue_info[queue_name][NMAPP] = {}
        self.queue_info[queue_name][NMAPP][ELAPSE] = float(this_queue[NMAPP])

        if self.queue_info[queue_name].get(NMACAPP) is None:
            self.queue_info[queue_name][NMACAPP] = {}
        self.queue_info[queue_name][NMACAPP][ELAPSE] = float(this_queue[NMACAPP])

        if self.queue_info[queue_name].get(NMPEAPP) is None:
            self.queue_info[queue_name][NMPEAPP] = {}
        self.queue_info[queue_name][NMPEAPP][ELAPSE] = float(this_queue[NMPEAPP])

        if self.queue_info[queue_name].get(NMCON) is None:
            self.queue_info[queue_name][NMCON] = {}
        self.queue_info[queue_name][NMCON][ELAPSE] = float(this_queue[NMCON])

        if self.queue_info[queue_name].get(USECP) is None:
            self.queue_info[queue_name][USECP] = {}
        self.queue_info[queue_name][USECP][ELAPSE] = float(this_queue[USECP])
