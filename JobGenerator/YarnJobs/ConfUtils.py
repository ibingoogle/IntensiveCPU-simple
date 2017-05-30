import time
import urllib2
import json
import random
import time

from operator import itemgetter


global START_TIME

START_TIME = time.time()

class Configure:

    confs = {}   #Dictionary

    confFile = "./conf"

    ##initialize with file name and read in file
    def __init__(self, confFile = None, confs = None):
        if confFile is not None:
            self.confFile = confFile
        if confs is not None:
            self.confs = confs
        self.initialize()

    ##read configuration from conf file, convert them to key-value format, store them in Dictionary confs
    def initialize(self): 
        try:
            file = open(self.confFile,"r")
            lines = file.readlines()
            for line in lines:
                #this line is commen
                if line.startswith("#"):
                    pass
                ##this line does not follow typical configuration
                elif "=" not in line:
                    pass
                else:
                    key    = line.split("=")[0].strip()
                    value  = line.split("=")[1].strip()
                    #print "key=", key
                    #print "value=", value
                    #if value contains more options
                    value_list = []
                    if "," in value:
                        value = value.split(",")  # return list
                        #print "~~~value=", value
                        value = list(map(lambda x:x.strip(),value))
                        #print "~~~~~~value=", value
                        value_list+=value
                    else:
                        value_list.append(value)
                    #print "value_list = ", value_list
                    self.confs[key] = value_list
            print "confs = " , self.confs
                        
        except (IOError, OSError) as error:
            print "error during initialize configure %s", error
            return False
        return True

    ## get configuration value corresponding to key
    def get(self,key):
        if self.confs.get(key) is None:
            return None
        try:
            if self.confs[key] is not None:
                return self.confs[key]
            else:
                return None
        except KeyError as error:
            print "error when try to get by key", error
        return None

    ## add new configuration into current key value Dictionary
    def addConf(self,key,value=None):
        self.confs[key] = value

    ## return the keys start with key_prefix
    def get_prefix(self,key_prefix):
        results = []    
        for key in self.confs.keys():
            if key.startswith(key_prefix):
                ## we only wanna key's lengh is one unit longer than key_prefix, like a.b.c for a.b, or a.b.c.d for a.b
                if len(key.split(".")) - len(key_prefix.split(".")) == 1:
                    results.append(key)
                else:
                    pass
            else:
                continue
        return results



def read_json_url(url):
    dict_read = {}
    try:
        # read the content from the website using urlopen() function from urllib2 mode
        url_content = urllib2.urlopen(url).read()
        # print "url_content = ", url_content
        # convert the content into Dictionary format
        dict_read = json.loads(url_content)
        # print "dict_read = ", dict_read
    except Exception as exceptMessage:
        print "read url error", exceptMessage
    return dict_read





class ParameterService:    ## read parameters from conf file based on PREFIX_NAME, could be generator or jobmaker....

    def __init__(self,conf,PREFIX_NAME):
        self.conf        = conf
        self.run_time    = int(self.conf.get("runtime")[0])  ## get run time
        print "ParameterService.runtime = ", self.run_time
        ## return the keys like PREFIX_NAME.parameters.interval and PREFIX_NAME.parameters.mean
        parameter_keys   = self.conf.get_prefix(PREFIX_NAME + ".parameters")
        print "parameter_keys = ", parameter_keys
        self.parameter_slice_set = {}  ## establish relationship between parameter key and slice value
        for parameter_key in parameter_keys:  ## process each parameter related key
            initial         = float(self.conf.get(parameter_key)[0])  ## inital value
            slice           = self.conf.get(parameter_key + ".slice")  ## get slice value
            print "parameter_key_slice = ", slice
            parameter_slice = ParameterSlice(
                                            name        = parameter_key,
                                            value       = initial,
                                            slices_new  = slice,
                                            run_time    = self.run_time
                                            )
            self.parameter_slice_set[parameter_key] = parameter_slice
        
    def get_parameter(self,name):
        find = False ## do not found the name
        for name_set in self.parameter_slice_set.keys(): ## iterate each parameter key
            print "name_set = ", name_set
            ## TODO we should consider this -1 index
            if name_set.split(".")[-1] == name:  ## extract the name_part from name_set and compared to name ??????
                find = True
                return self.parameter_slice_set[name_set].get_current_value() ## get current value from parameterSlice
        if find == False:
            raise Exception("parameter not found exception")
        return None

class ParameterSlice: ## parameter slice value corresponding to parameter key

    ## slice format should be:
    ## 0.1:5, 0.2:10, 0.2:20 which means at the 10 percent of execution time, values turned to be 5
    def __init__(self,name,value,run_time,slices_new=None):
        print "ParamaterSlice.__init__"
        assert(name is not None)
        assert(value is not None)
        assert(run_time > 0)
        self.name       = name ## the key name
        self.initial    = value ## inital value
        self.mult_slice = True ## whether the slices_new is None
        self.slices     = []  ## store the slice info
        ## which means inital value
        self.current_slice = 0   ## this is index for slices
        self._add_slice_(slices_new)
        self.runtime    = run_time

    def _add_slice_(self,slices_new):
        if slices_new is None:
            self.mult_slice = False
            return
        for term in slices_new:   ## profess each element in slices_new
            time    = float(term.split(":")[0]) ## the time range should be 0~1
            if time < 0 or time > 1:
                raise Exception("illegale parameter negative value or larger than 1")
            value   = float(term.split(":")[1]) ## get value correponding to certain time
            if value < 0:
                raise Exception("illegale parameter negative value")
            print "time = ", time
            print "value = ", value
            new_term = (time,value)
            self.slices.append(new_term) ## add slice info into self.slices
        ini_term = (0,self.initial) ## convert inital value to slice info format
        self.slices.append(ini_term) ## add initial info into self.slices
        ### sort based on time
        self.slices.sort(key=itemgetter(0))
            
                
    def get_current_value(self):
        if self.mult_slice is False:   ## value never change
            return self.initial
        ## compute progress
        global START_TIME
        progress = (time.time() - START_TIME) * 1.0 /self.runtime
        
        ##TODO we should consider current_slice + 2 or more
        if self.current_slice < len(self.slices) - 1 and progress > self.slices[self.current_slice+1][0]: ## ????????????
            self.current_slice = self.current_slice + 1
        return self.slices[self.current_slice][1]

##for test only
if __name__=="__main__":
    url="http://192.168.2.20:8088/ws/v1/cluster/info"
    read_json_url(url)
