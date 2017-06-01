import urllib.request
import urllib.parse
import sys
import http.client
import json
import xmltodict

class HttpPost:

	host = ""
	port = 80
	conf = "/conf"
	form = "xml"
	Headers = {} # used in urllib.request.Request()
	url = ""
	post_content = {'user':'shaoqiwang','host':'hadoop2master','port':'10002'}

	def __init__(self):
		self.load_conf()
		self.url = "http://" + self.host + ":" + str(self.port)
		self.Headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
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

	def post(self):
		try:
			# convert the dict_data into string form, the data will be reversed in the http server
			data = urllib.parse.urlencode(self.post_content)
			data = data.encode("ascii")
			# send POST command
			req = urllib.request.Request(self.url,data)
			response = urllib.request.urlopen(req)
		except http.client.HTTPException as error:
			print ("error: ", error)


if __name__ == "__main__":
	TheHttpPost = HttpPost()
	
	TheHttpPost.post()
