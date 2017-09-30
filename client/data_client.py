import numpy as np
import rpyc
import time
import threading
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

hostname = '127.0.0.1'
port = 18861


if __name__=='__main__':
	c = rpyc.connect(hostname,port)
	service = c.root.get_shared()
	times = 1
	for n in range(times):
		my_random =StringIO(service.send_random())
		my_array = np.load(my_random)['frame']
		print(my_array)
