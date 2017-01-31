
import numpy as np
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

def run(n):

	lidar = RPLidar(PORT_NAME)
	data = []
	try:
		print('Recording measurements. . .')
		scan_count = 0
		for scan in lidar.iter_scans():
			data.append(np.array(scan))
			scan_count += 1
			if scan_count > n:
				
				lidar.stop()
				lidar.disconnect()
				return np.array(data)
				break
	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()
	


