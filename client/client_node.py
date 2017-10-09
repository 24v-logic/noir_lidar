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

class my_client():
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
	my_client = my_client()
	c1 = rpyc.connect(hostname,port)
	server1 = c1.root
	my_client.add_shared_service(server1.get_node("node01"))
	my_client.add_shared_service(server1.get_node("node02"))

	for service_key in my_client.services:
		my_client.services[service_key].print_tag()
		my_client.services[service_key].print_string("hello")
		print(rx_random(my_client.services[service_key]))
		raw_input()
	server1.list_nodes()

	'''
	port = 18862
	c2 = rpyc.connect(hostname,port)
	server2= c2.root
	my_client.add_shared_service(server2.get_shared())
	for service_key in my_client.services:
		my_client.services[service_key].print_tag()
		raw_input()
	'''

	'''
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	times = 1
	for n in range(times):
		service.test()
		service.print_tag()
		service.print_string("Hello, World")
		print(service.tag)
		print("done")
	'''
