import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,4)

ax1.set_title("RGB")
ax2.set_title("Luminance")
ax3.set_title("Spectral Luminance")

ims = []
frames = np.load('frames.npy')

lum_frames = []
lum_ims = []
spectral_ims = []

for frame in frames:
	lum_frames.append(frame[:,:,0])

plt.sca(ax1)
for i in range(len(frames)):
    im = plt.imshow(frames[i], animated=True)
    ims.append([im])

#ani1 = animation.ArtistAnimation(fig, ims, interval=500, blit=True,repeat_delay=1000)


plt.sca(ax2)                                
for i in range(len(frames)):
    im = plt.imshow(lum_frames[i], animated=True)
    lum_ims.append([im])

#ani2 = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=1000)
plt.sca(ax3)                               
for i in range(len(frames)):
    im = plt.imshow(lum_frames[i], animated=True)
    spectral_ims.append([im])
    im.set_cmap('nipy_spectral')
#ani3 = animation.ArtistAnimation(fig, ims, interval=500, blit=True,repeat_delay=100)

#ani1.save('dynamic_images.mp4')

plt.show()