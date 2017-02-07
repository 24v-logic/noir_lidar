import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

ax = plt.subplot(111, projection='polar')

data = np.load('lidar_frames.npy')[1]
print(data)
ax.scatter(np.radians(data[:,1]),data[:,2])


plt.show()