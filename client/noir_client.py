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

hostname = '192.168.1.5'
port = 18861

if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	while True:
		lidar_frames, camera_frames = hi_speed_capture(10,3)
		lidar_payload = payloadize(lidar_frames)
		camera_payload = payloadize(camera_frames)
		service.acquire_frames('lidar_frames1', lidar_payload)
		service.acquire_frames('camera_frames1', camera_payload)
		break
