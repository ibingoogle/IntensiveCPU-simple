#!/bin/Python
from __future__ import print_function
import Pyro4


# derived from object is the new feature of Python 3
@Pyro4.expose
class Warehouse(object):

	def __init__(self):
		self.contents = ["chair", "bike", "flashlight", "laptop", 'couch']

	def list_contents(self):
		return self.contents

	def take(self, name, item):
		self.contents.remove(item)
		print("{0} took the {1}.".format(name, item))

	def store(self, name, item):
		self.contents.append(item)
		print("{0} stored the {1}.".format(name, item))
