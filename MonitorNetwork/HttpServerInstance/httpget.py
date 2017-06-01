import urllib.request
import sys
import http.client
import json
import xmltodict

class HttpGet:

	host = ""
	port = 80
	conf = "/conf"
	form = "xml"
	Headers = {} # used in urllib.request.Request()
	url = ""

	def __init__(self):
		self.load_conf()
		self.url = "http://" + self.host + ":" + str(self.port)
		#self.Headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		self.Headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0'}
		print(self.url)
		#self.Headers = {"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

	def load_conf(self):
		current_path = sys.path[0]
		try:
			file = open(current_path + self.conf, "r")
			self.host = file.readline().split("=")[1].strip("\n")
			self.port = int(file.readline().split("=")[1].strip("\n"))
			self.form = file.readline().split("=")[1].strip("\n")
		except (IOError,OSError) as error:
			print("error during conf loading %s", error)
			file.close()

	def read_url(self):
		dict_read = {}
		if self.form == "json":
			dict_read = self.read_json_url() # based on urllib.request.Request() and .urlopen(), using Headers
		else:
			dict_read = self.read_xml_url() # only using urllib.request.urlopen(), no Headers (not work, TBD)
		print(dict_read)

	def read_json_url(self): #(except happens, but still can get the data in exceptMessage)
		dict_read = {}
		try:
			req = urllib.request.Request(self.url, headers=self.Headers)
			response = urllib.request.urlopen(req)
			read = response.read()
			dict_read = json.loads(read)
			response.close()
		except http.client.HTTPException as exceptMessage:
			dict_read = json.loads(str(exceptMessage))
			print ("error")
		return dict_read

	def read_xml_url(self): #(not work, TBD)
		dict_read = {}
		try:
			#req = urllib.request.Request(self.url, headers=self.Headers)
			#response = urllib.request.urlopen(req)
			response = urllib.request.urlopen(self.url)
			print ("~~~~~~~~~~~~~~~~~")
			order_dict_read = xmltodict.parse(response.read())
			json_read = json.dumps(order_dict_read)
			dict_read = json.loads(json_read)
			response.close()
		#except http.client.HTTPException as exceptMessage:
		except urllib.error.HTTPError as e:
			print("read url error: ", e)
		return dict_read


if __name__ == "__main__":
	TheHttpGet = HttpGet()
	
	TheHttpGet.read_url()
