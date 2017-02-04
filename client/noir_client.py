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

def double_capture(n_frames):
	lidar = RPLidar('/dev/ttyUSB0')
	lidar_data = []
	cam_data = []
	try:
		print('Capturing data')
		scan_count = 0
		for scan in lidar.iter_scans():
			with picamera.PiCamera() as camera:
				with picamera.array.PiRGBArray(camera) as output:
					camera.resolution = (720,600)
					camera.capture(output,'rgb')
					cam_data.append(output.array)
			lidar_data.append(np.array(scan))
			scan_count+=1
			if scan_count > n_frames:
				break
		data_array = np.array([cam_data,lidar_data])
		f = StringIO()
		np.savez_compressed(f, frame=output.array)
		f.seek(0)
		return(f.read())

hostname = '192.168.1.5'
port = 18861

if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	while True:
		service.acquire_frames('double_capture',double_capture(3))
		#service.acquire_frames('camera_frames', capture_camera(10))
		#service.acquire_frames('lidar_frames', capture_lidar(10))
		
		break
