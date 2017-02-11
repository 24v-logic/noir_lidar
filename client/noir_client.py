import numpy as np
import rpyc
import picamera
import picamera.array
import thread
import time
import threading
import noir_lidar
from cStringIO import StringIO

import sys
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle']=True
'''
STDERR = sys.stderr
def excepthook(*args):
	print >> STDERR, 'caught'
	print >> STDERR, args
sys.excepthook = excepthook
'''


def payloadize(npyarray):
	npyarray = np.array(npyarray)
	f = StringIO()
	np.savez_compressed(f,frame=npyarray)
	f.seek(0)
	return f.read()

hostname = '192.168.1.4'
port = 18861

if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	times = 20
	for n in range(times):
		
		lidar_frames, camera_frames = noir_lidar.variable_capture(100,3,(n+1)*64,(n+1)*48)
		lidar_payload = payloadize(lidar_frames)
		camera_payload = payloadize(camera_frames)
		service.acquire_frames('test1_lidar_frames' + str(n), lidar_payload)
		service.acquire_frames('test1_camera_frames' + str(n), camera_payload)
		
