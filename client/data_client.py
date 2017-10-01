import numpy as np
import rpyc
import time
import threading
from cStringIO import StringIO
import sys
import matplotlib.pyplot as plt
import cv2
#plt.ion()
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle']=True


'''
STDERR = sys.stderr
def excepthook(*args):
	print >> STDERR, 'caught'
	print >> STDERR, args
sys.excepthook = excepthook
'''

hostname = '192.168.1.11'
port = 18861

fig = plt.figure()

def image_proc(img):
	for frame in img:
		cv2.dilate(frame,None)
		cv2.erode(frame,None)
		cv2.imshow("my_image",frame)
		cv2.waitKey(0)
if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	times = 1
	for n in range(times):
		my_random = StringIO(service.send_random())
		#my_array = np.load(my_random)['frame']
		my_array = StringIO(service.send_images(3))
		print("data acquired")
		my_images = np.load(my_array)['frame']
		#print(my_images)
		#print(my_image[0].shape)
		#plt.imshow(my_image[0], interpolation='nearest')
		#plt.show()
		#raw_input("...")
		image_proc(my_images)
		print("done")
