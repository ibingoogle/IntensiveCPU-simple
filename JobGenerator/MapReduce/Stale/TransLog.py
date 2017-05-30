import time
import os

class AutoProcess:
    done_intermediate_path = ""
    done_path_base = ""
    desktop_path = ""
    source_path = ""
    destination_path = "" 

  
    def __init__(self):
        self.done_intermediate_path = "/tmp/hadoop-yarn/staging/history/done_intermediate/hadoop0master/"
        self.done_path_base = "/tmp/hadoop-yarn/staging/history/done/"
        self.desktop_path = "/home/hadoop0master/Desktop/jhist/"
        self.source_path = "/home/hadoop0master/Desktop/jhist/jobs*.jhist"
        self.destination_path = "sean@128.198.180.112:/home/sean/workspace/Python/LogAnalysis/jobs/"
       
    def rename(self):
        path = self.desktop_path
        count = 1
        filelist = os.listdir(path)
        for files in filelist:
            Olddir = os.path.join(path,files)
            if os.path.isdir(Olddir):
                continue
            filename = os.path.splitext(files)[0]
            filetype = os.path.splitext(files)[1]
            if filetype == ".jhist":
                Newdir = os.path.join(path,"jobs"+str(count)+filetype)
                os.rename(Olddir,Newdir)
                count+=1


    def pull(self):
        command_pull = "hdfs dfs -get" + " " + self.done_intermediate_path + "*.jhist" + " " + self.desktop_path
        print "command_pull: ", command_pull
        os.system(command_pull)

 
    def scp(self):
        command_scp = "scp" + " " + self.source_path + " " + self.destination_path
        print "command_scp: ", command_scp
        os.system(command_scp)
    
    def delete_local(self):
        command_delete_local = "rm -rf" + " " + self.source_path
        print "command_delete_local: ", command_delete_local
        os.system(command_delete_local)

    def move_delete_hdfs(self):
        done_path = self.done_path_base + local_time()
        command_move_jhist = "hdfs dfs -mv" + " " + self.done_intermediate_path + "*.jhist" + " " + done_path
        print "command_move_jhist: ", command_move_jhist
        os.system(command_move_jhist)
        command_move_xml = "hdfs dfs -mv" + " " + self.done_intermediate_path + "*.xml" + " " + done_path
        print "command_move_xml: " + command_move_xml
        os.system(command_move_xml)
        command_delete_summary = "hdfs dfs -rm" + " " + self.done_intermediate_path + "*.summary"
        print "command_delete_summary: " + command_delete_summary
        os.system(command_delete_summary)

def local_time(): 
    time_array = time.localtime()
    year = str(time_array[0])
    if time_array[1] < 10:
        month = "0" + str(time_array[1])
    else:
        month = str(time_array[1])
    if time_array[2] < 10:
        day = "0" + str(time_array[2])
    else:
        day = str(time_array[2])
    end = "000000"
    time_path = year + "/" + month + "/" + day + "/" + end + "/"
    print "time_path: " + time_path
    return time_path

if __name__ == "__main__":
    auto_process = AutoProcess()
    auto_process.delete_local()
    auto_process.pull()
    auto_process.rename()
    auto_process.scp() 
    auto_process.move_delete_hdfs()
