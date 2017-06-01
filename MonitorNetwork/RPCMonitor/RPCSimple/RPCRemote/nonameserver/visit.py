# This is the code that runs this example.
# visit.py is the RPC client, use the class in RPC server through Pyro4.Proxy
# run visit.py in local node (192.168.2.30)

import sys
import Pyro4

from person import Person
sys.excepthook = Pyro4.util.excepthook

# get warehouse class from remote machine
warehouse = Pyro4.Proxy("PYRONAME:warehouse")
janet = Person("Janet")
henry = Person("Henry")
janet.visit(warehouse)
henry.visit(warehouse)
