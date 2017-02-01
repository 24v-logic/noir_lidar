import thread
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
from cStringIO import StringIO
import threading
'''rpyc server for data collection'''
import rpyc

#rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
figure = []
class shared_data_acquisition_class():
	def __init__(self):
		print("Data Acquisition Service is running. . .")

	def acquire_frames(self,outfile,new_data):
		an_array = np.load(StringIO(new_data))['frame']

		o = outfile

		if isinstance(an_array,np.ndarray):
			print"saving array as %s" % o
			np.save(o,an_array)
		else:
			print("not a numpy array")
			print(type(self.data))
		
	def get_img(self,data):
		img = np.load(StringIO(data))['frame']
		imgplot = plt.imshow(img)
		print"image plotted"
	
	def get_string(self,string):
		f = open('string.txt','w')
		f.write(string)

	def what_is(self, thing):
		print(type(thing))

s = shared_data_acquisition_class()

class shared_data_acquisition_service(rpyc.Service):
	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')

	def exposed_get_shared(self):
		return s

def arbitrary_threaded_task( threadName, delay):
	count = 0
	while count < 100:
		time.sleep(delay)
		count +=1
		print"%s, %s" % (threadName, time.ctime(time.time()))



if __name__=='__main__':
	print("Starting main...")
	from rpyc.utils.server import ThreadedServer
	'''start threaded rpyc server'''
	t = ThreadedServer(shared_data_acquisition_service, port=18861,protocol_config={"allow_public_attrs": True})

	try:
		print("Starting threads...")
		print("Starting arbitrary threaded task")
		thread.start_new_thread( arbitrary_threaded_task,("thread-1", 5,))
		print("Starting rpyc server")
		thread.start_new_thread(t.start,())
		
		
	except:
		print("error")

	while 1:
		pass

