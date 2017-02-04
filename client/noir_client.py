import numpy as np
import rpyc
import picamera
import picamera.array
import thread
import time
import threading
from rplidar import RPLidar

from cStringIO import StringIO
from lidar_get import run
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle']=True
output = []
lidar_frames = []
cam_frames = []
import sys
'''
STDERR = sys.stderr
def excepthook(*args):
	print >> STDERR, 'caught'
	print >> STDERR, args
sys.excepthook = excepthook
'''
def capture():

	with picamera.PiCamera() as camera:
		with picamera.array.PiRGBArray(camera) as output:
			camera.resolution = (1280,700)
			camera.capture(output,'rgb')
			print('Captured %d%d image' % (output.array.shape[1], output.array.shape[0]))
			f = StringIO()
			np.savez_compressed(f, frame=output.array)
			f.seek(0)
			return(f.read())


def capture_camera(n):
	print("camera")
	frames = []
	with picamera.PiCamera() as camera:
		with picamera.array.PiRGBArray(camera) as output:
			camera.resolution = (640,480)
			for i in range(n):
				camera.capture(output, 'rgb')
				frames.append(output.array)
				output.truncate(0)
				
	print("captured %s frames" % (n))
	f = StringIO()
	np.savez_compressed(f,frame=frames)
	f.seek(0)
	print "camera capture done"
	return f.read()
			
def capture_lidar(n):
	print("lidar")
	lidar_data = run(n)
	f = StringIO()
	np.savez_compressed(f, frame=lidar_data)
	f.seek(0)
	print "lidar capture done"
	return f.read()

def payloadize(npyarray):
	npyarray = np.array(npyarray)
	f = StringIO()
	np.savez_compressed(f,frame=npyarray)
	f.seek(0)
	return f.read()

hostname = '192.168.1.5'
port = 18861

if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	while True:
		service.acquire_frames('camera_frames',capture_frames(10))
		#service.acquire_frames('camera_frames', capture_camera(10))
		#service.acquire_frames('lidar_frames', capture_lidar(10))
		
		break
