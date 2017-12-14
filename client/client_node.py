import numpy as np
import rpyc
import time
import threading
from cStringIO import StringIO
import sys
import logging

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle']=True


'''
STDERR = sys.stderr
def excepthook(*args):
	print >> STDERR, 'caught'
	print >> STDERR, args
sys.excepthook = excepthook
'''

def get_connection(hostname, port):
	c = rpyc.connect(hostname,port)
	server = c.root
	return server

class client():
	def __init__(self):
		self.services = {}

	def add_shared_service(self, service):
		self.services.update({service.tag : service})
		print self.services

def rx_random(service):
	random = np.load(StringIO(service.tx_random()))['frame']
	return(random)

if __name__=='__main__':
	hostname = '127.0.0.1'
	port = 18861

	my_client = client()
	print("client initialized", my_client)
	raw_input("press any key to continue")
	c1 = rpyc.connect(hostname,port)
	print("connected to %s, %s" % (hostname, port))
	raw_input("press any key to continue")
	server1 = c1.root
	service_nodes = ["node01","node02"]
	for each in service_nodes:
		print("Adding shared service node %s" % each)
		my_client.add_shared_service(server1.get_node(each))
		raw_input("press any key to continue")

	for service_key in my_client.services:
		print("printing tag for %s" % service_key)
		my_client.services[service_key].print_tag()
		raw_input("press any key to continue")
		print("printing string for %s" % service_key)
		my_client.services[service_key].print_string("hello world")
		raw_input("press any key to continue")

		print("Receiving random 320x240x4 numpy array from %s" % service_key)
		print(rx_random(my_client.services[service_key]))
		raw_input("press any key to continue")
	print("listing nodes on server1")
	server1.list_nodes()
