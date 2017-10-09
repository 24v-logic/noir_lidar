import time
import numpy as np
from cStringIO import StringIO
import thread
import threading
'''rpyc server for sensor data collection'''
import rpyc
import multiprocessing as mup
import logging
from rpyc.utils.server import ThreadedServer
import sys
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
figure = []
'''
STDERR = sys.stderr
def excepthook(*args):
	print >> STDERR, 'caught'
	print >> STDERR, args
sys.excepthook = excepthook
'''
class my_node():
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

class my_node_service(rpyc.Service):
	nodelist = []

	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')

	def exposed_get_node(self, client_tag):
		new_node = my_node(client_tag)
		self.nodelist.append(new_node)
		return new_node

	def exposed_list_nodes(self):
		for node in self.nodelist:
			print(node.tag)

if __name__=='__main__':
	print("Starting main...")
	my_args = sys.argv

	try:
		print("Starting threads...")
		print("Starting rpyc server")
		t1 = ThreadedServer(my_node_service,hostname="127.0.0.1", port=18861,protocol_config={"allow_public_attrs": True})
		thread.start_new_thread(t1.start,())
		'''
		t1 = ThreadedServer(my_node_service,hostname="127.0.0.1", port=18861,protocol_config={"allow_public_attrs": True})
		thread.start_new_thread(t1.start,())

		n = my_node("node01")
		t2 = ThreadedServer(my_node_service,hostname="127.0.0.1", port=18862,protocol_config={"allow_public_attrs": True})
		thread.start_new_thread(t2.start,())
		'''
	except:
		print("error")

	while 1:
		pass
