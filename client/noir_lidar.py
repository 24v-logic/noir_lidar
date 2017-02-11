
import numpy as np
from rplidar import RPLidar
import picamera

PORT_NAME = '/dev/ttyUSB0'

def lidar_capture(n):

	lidar = RPLidar(PORT_NAME)
	data = []
	try:
		print('Recording lidar scans. . .')
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

def image_capture(n):
	print('Recording camera images')
	camera_frames = []
	with picamera.PiCamera() as camera:
		with picamera.array.PiRGBArray(camera) as output:
			#camera configuration
			camera.resolution = (640,480)
			camera.capture(output, 'rgb')
			for i in range(n):
				camera.capture(output,'rgb')
				camera_frames.append(output.array)
				output.truncate(0)
	return np.array(camera_frames)

def variable_capture(n,m,i,j):
	lidar = RPLidar(PORT_NAME)
	lidar_frames = []
	image_frames = []
	try:
		print('Recording lidar scans and camera images. . .')
		scan_count = 0
		for scan in lidar.iter_scans():
			with picamera.PiCamera() as camera:
				with picamera.array.PiRGBArray(camera) as output:
					for i in range(m):
						camera.resolution=(i,j)
						camera.capture(output,'rgb')
						image_frames.append(output.array)
						output.truncate(0)
			lidar_frames.append(np.array(scan))
			scan_count += 1
			if scan_count > n:
				lidar.stop()
				lidar.disconnect()
				return np.array(lidar_frames), np.array(image_frames)
				break

	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()

def hi_speed_capture(n,m):
	lidar = RPLidar(PORT_NAME)
	lidar_frames = []
	image_frames = []
	try:
		print('Recording lidar scans and camera images. . .')
		scan_count = 0
		for scan in lidar.iter_scans():
			with picamera.PiCamera() as camera:
				with picamera.array.PiRGBArray(camera) as output:
					for i in range(m):
						camera.resolution=(64,48)
						camera.capture(output,'rgb')
						image_frames.append(output.array)
						output.truncate(0)
			lidar_frames.append(np.array(scan))
			scan_count += 1
			if scan_count > n:
				lidar.stop()
				lidar.disconnect()
				return np.array(lidar_frames), np.array(image_frames)
				break

	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()


def double_capture(n):
	lidar = RPLidar(PORT_NAME)
	lidar_frames = []
	image_frames = []
	try:
		print('Recording lidar scans and camera images. . .')
		scan_count = 0
		for scan in lidar.iter_scans():
			with picamera.PiCamera() as camera:
				with picamera.array.PiRGBArray(camera) as output:
					camera.resolution=(640,480)
					camera.capture(output,'rgb')
					image_frames.append(output.array)
					output.truncate(0)
			lidar_frames.append(np.array(scan))
			scan_count += 1
			if scan_count > n:
				lidar.stop()
				lidar.disconnect()
				return np.array(lidar_frames), np.array(image_frames)
				break

	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()
