import time
import numpy as np
from cStringIO import StringIO
import threading
'''rpyc server for sensor data collection'''
import rpyc
import picamera
import picamera.array

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
figure = []

class data_collector():
	def __init__(self):
		print("Data collector running")

	def test(self):
		print("test")

	def send_images(self,n):
		image_array = self.capture_images(n,1/30)
		f = StringIO()
		np.savez_compressed(f, frame=image_array)
		f.seek(0)
		return f.read()

	def send_random(self):
		npyarray = np.random.rand(10,10,4)
		f = StringIO()
		np.savez_compressed(f, frame=npyarray)
		f.seek(0)
		return f.read()

	def capture_images(self,n,delay):
		camera_frames = []
		with picamera.PiCamera() as camera:
			with picamera.array.PiRGBArray(camera) as output:
				for i in range(n):
					camera.resolution = (320,240)
					camera.capture(output, 'bgr')
					camera_frames.append(output.array)
					output.truncate(0)
					time.sleep(delay)
					print("capture %d" % i)
				print("captures done")
		return np.array(camera_frames)

d = data_collector()

class data_collector_service(rpyc.Service):
	def on_connect(self):
		print('connected')

	def on_disconnect(self):
		print('disconnected')

	def exposed_get_shared(self):
		return d

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
	t = ThreadedServer(data_collector_service, port=18861,protocol_config={"allow_public_attrs": True})

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
