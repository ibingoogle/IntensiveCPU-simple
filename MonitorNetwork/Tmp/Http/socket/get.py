import urllib.request
import sys
import http.client
import json
import xmltodict


def read_json_url(url):
    try:
        Headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6', 'Referer': 'http://hadoop2master:10000' , 'Connection': 'close'}
        Headers = {'Host':'hadoop2master:10000', 'Connection': 'close', 'Accept-Encoding' : 'identity'}
        dict_read = {}
        print("11111111111100000000000000000")
        req = urllib.request.Request(url,headers=Headers)
        print("0000000000000000000000000000000000")
        #print(req)
        response = urllib.request.urlopen(req)
        print("1111111111111111111111111111")
        read = response.read()
        dict_read = json.loads(read)
    except http.client.HTTPException as exceptMessage:
        print("222222222222222222222222222222222")
        print(str(exceptMessage))
        dict_read = json.loads(str(exceptMessage))
    return dict_read

def read_xml_url(url):
    dict_read = {}
    try:
        response  = urllib.request.urlopen(url)
        order_dict_read = xmltodict.parse(response.read())
        json_read = json.dumps(order_dict_read)
        dict_read = json.loads(json_read)
    except Exception as exceptMessage:
        print("read url error",exceptMessage)
    finally:
        response.close()
    return dict_read



headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  

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

# get dict_read
dict_read = {}
if form == "json":
    dict_read = read_json_url(url)
else:
    dict_read = read_xml_url(url)
       
print(dict_read)

