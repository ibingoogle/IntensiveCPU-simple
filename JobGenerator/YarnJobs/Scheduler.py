import ConfUtils
import time
import Monitor
import Generator

global START_TIME

START_TIME = time.time() ## get current time starting from 1970 at the very begining

class SchedulerPlan:


    def __init__(self):
        ##global variable, we only have one plan at any time 
        self.conf = ConfUtils.Configure() # load configuration from conf file
        self.cluster_url = self.conf.get("hadoop.url")[0] + "/ws/v1/cluster/info"
        print "self.cluster_url = ", self.cluster_url


        ##read cluster information through Yarn's ResourceManager REST API's in JSON format
        ##check the cluster is running
        clusterInfo = ConfUtils.read_json_url(self.cluster_url)
        if clusterInfo.get("clusterInfo") is None:
            raise Exception("cluster is not running")

        
        #try to make Queue Monitor objects
        scheduler_type = Monitor.Monitor.get_scheduler_type(self.conf) # get the schedule type in the cluster
        if scheduler_type == "capacityScheduler":
            self.monitor = Monitor.CapacityQueueMonitor(self.conf)
        elif scheduler_type == "fifoScheduler":
            self.monitor = Monitor.FifoQueueMonitor(self.conf)
        else:
            raise Exception("scheduler is not supported")

        ## monitor queue for the first time
        self.monitor.monitor_queue()
        ## start the moniting thread
        self.monitor.start()
        time.sleep(2)
        self.monitor.stop()


        self.generators = []
        ## try to make generator
        generator_types = []
        generator_types += self.conf.get("generators")
        print "generator_types: ", generator_types
        if len(generator_types) is 0:
            raise Exception("missing generator")

        for generator_type in generator_types:
            if generator_type.startswith("OrderGenerator"):
                generator = Generator.OrderGenerator(generator_type,self.conf,self.monitor)
                ##TODO log
                print "generator: OrderGenerator"
            elif generator_type.startswith("PoissonGenerator"):
                generator = Generator.PoissonGenerator(generator_type,self.conf,self.monitor)
                ##TODO log
                print "generator: PoissonGnenrator"
            elif generator_type.startswith("CapacityGenerator"):
                generator = Generator.CapacityGenerator(generator_type,self.conf,self.monitor)
                ##TODO log
                print "generator: CapacityGenerator"
            else:
                raise Exception("unknown generator")
            self.generators.append(generator)

        ##get run time
        self.run_time = int(self.conf.get("runtime")[0])
        #assert(self.run_time > 100)

if __name__ == "__main__":

    Scheduler_plan = SchedulerPlan()
