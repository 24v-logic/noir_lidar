import numpy as np
import rpyc
import time
import thread
from cStringIO import StringIO
import sys
import logging
from rpyc.utils.server import ThreadedServer

#Server node
class node():
	def __init__(self,my_tag):
		self.tag = my_tag
		print("initializing %s " % my_tag)

	def test(self):
		print("test")

	def print_tag(self):
		print(self.tag)

	def print_string(self, string):
		print(string)

	def tx(self, data):
		f = StringIO()
		np.savez_compressed(f, frame=data)
		f.seek(0)
		return f.read()

	def tx_random(self):
		random_data = np.random.rand(320,240,4)
		print("%s sending random data" % self.tag)
		return self.tx(random_data)

class node_service(rpyc.Service):
	nodelist = []

	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')

	def exposed_get_node(self, client_tag):
		new_node = node(client_tag)
		self.nodelist.append(new_node)
		return new_node

	def exposed_list_nodes(self):
		print("Node list:")
		for node in self.nodelist:
			print(node.tag)

#Client

class client():
	def __init__(self):
		self.services = {}

	def add_shared_service(self, service):
		self.services.update({service.tag : service})
		print self.services

def rx_random(service):
	random = np.load(StringIO(service.tx_random()))['frame']
	return(random)
