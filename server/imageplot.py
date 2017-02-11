import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

fig = plt.figure()

ax1 = fig.add_subplot(1,2,1)

ax2 = plt.subplot(122,projection='polar')


camera_frames = np.load('camera_frames2.npy')
lidar_frames = np.load('lidar_frames2.npy')
rotated_camera_frames = []
lum_frames = []


plt.sca(ax1)
ims = []
for frame in range(len(camera_frames)):
	rotated_image = ndi.rotate(camera_frames[frame],180)
	rotated_camera_frames.append(rotated_image)
	lum_frames.append(rotated_image[:,:,0])
	im = plt.imshow(lum_frames[frame], animated=True)
	ims.append([im])

lidar_ims= []

plt.sca(ax2)
for frame in range(len(lidar_frames)):
	thetas = np.radians(lidar_frames[frame][:,1])
	rs = lidar_frames[frame][:,2]
	lidar_frame = np.array([[thetas],[rs]])
	lidar_im = plt.scatter(thetas,rs)
	lidar_ims.append(lidar_im)

ani1 = animation.ArtistAnimation(fig,ims,interval=50, blit=True, repeat_delay=0)
#ani2 = animation.ArtistAnimation(fig,lidar_ims,interval=50,repeat_delay=0)
plt.show()
ani1.save('capture2.mp4')
'''
class SubplotAnimation(animation.TimedAnimation):
	def __init__(self):
		fig = plt.figure()
		ax1 = fig.add_subplot(1,2,1)
		ax2 = fig.add_subplot(2,2,2)

		self.t = range(len(frames))

	def _draw_frame(self,framedata):
		i = framedata
		head = i-1
		head_slice = (self.t > self.t[i]-1) & (self.t < self.t[i])
'''
