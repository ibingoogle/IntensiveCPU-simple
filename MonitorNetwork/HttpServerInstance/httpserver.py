import socket
import re
import json
import xmltodict
import sys
import os
from threading import Thread



class HttpServer(Thread):

	host = ""
	port = 80
	conf = "/conf"
	form = "xml"
	post_content = {'user':'swang', 'a':'1', 'b':'2'}

	def __init__(self):
		Thread.__init__(self)
		self.load_conf()
		# create a socket instance to communicate, prototype: int socket(int domain, int type, int protocol=0)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# set socket to reuse the address
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# bind host and port address
		self.sock.bind((self.host, self.port))
		# socket to listen
		self.sock.listen(1)

	def start(self):
		Thread.start(self)

	def run(self):
		index = 1
		#infinite loop
		while True:
			index = index + 1
			# self.post_content['user'] = str(index)
			# waiting to accept the request such as get/post/refresh browser
			conn, addr = self.sock.accept()			
			# maximum number of requests waiting
			request = conn.recv(1024)
			request_str = str(request, encoding="utf-8")
			
			print ('Connect by: ', addr)
			print ('Request is:\n', request)

			# convert dict to json or xml form
			content = self.convert_content(self.post_content)

			print ("content = ", content)
			conn.sendall(bytes(content, encoding="utf-8"))
			# close connection
			conn.close()


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


	def convert_content(self,post_content):
		if self.form == "json":
			converted_content = self.to_json(post_content)
			return converted_content
		converted_content = self.to_xml(post_content)
		return converted_content

	def to_json(self,dict_content):
		jdata = json.dumps(dict_content)
		return jdata

	def to_xml(self,dict_content):
		# add an root
		dict_root = {}
		dict_root['root'] = dict_content
		converted_content = xmltodict.unparse(dict_root)
		return converted_content	


if __name__ == "__main__":
	#write pid to the file
	process_id = os.getpid()
	pid_file = sys.path[0]
	try:
		file = open(pid_file + "/httpserver_pid", "w")
		file.write(str(process_id))
	except (IOError,OSError) as error:
		print("error during pid file writting %s", error)
		file.close()

	TheHttpServer = HttpServer()
	TheHttpServer.start()

	print("HttpServer begins working")
	print("Address is:",TheHttpServer.host,":",TheHttpServer.port)
