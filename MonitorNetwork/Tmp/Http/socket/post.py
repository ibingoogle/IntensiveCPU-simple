import socket
import re
import urllib.request
import urllib.parse
import json
import time
import http.client
import sys

# load conf file
cur_path = sys.path[0]
try:
    file = open(cur_path + "/conf", "r")
    HOST = file.readline().strip("\n")
    PORT = int(file.readline().strip("\n"))
    form = file.readline().split("=")[1].strip("\n")
except (IOError,OSError) as error:
    print("error during conf loading %s", error)

# get url
url='http://' + HOST + ":" + str(PORT)

post_content ={'user':'shaoqiwang'}
data = urllib.parse.urlencode(post_content)
#jdata = json.dumps(post_content)
#binary_data = bytes(post_content, encoding = 'utf-8')

#print ("000000000000000000000000000000")
try:
    Headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6', 'Referer': 'http://hadoop2master:10000' , 'Connection': 'close', 'Content-Length' : '22'}
    data = data.encode('ascii')
    response = urllib.request.urlopen(url, data, headers=Headers)
except http.client.HTTPException as error:
    print ("1111111111111111111: ", error)

#response = urllib.request.urlopen(req)
