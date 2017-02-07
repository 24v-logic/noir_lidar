import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)

frames = np.load('image_frames.npy')

im = frames[0]

image = plt.imshow(im)

plt.show()