#!/bin/python

from __future__ import print_function
import sys

if sys.version_info < (3, 0):
	input = raw_input

# derived from object is the new feature of Python 3
class Person(object):
