import numpy as np
import matplotlib.pyplot as plt
import OPTICS as OP
from itertools import *

# generate some spatial data with varying densities
np.random.seed(0)

n_points_per_cluster = 250

X = np.empty((0, 2))
X = np.r_[X, [-5,-2] + .8 * np.random.randn(n_points_per_cluster, 2)]

X = np.r_[X, [4,-1] + .1 * np.random.randn(n_points_per_cluster, 2)]

X = np.r_[X, [1,-2] + .2 * np.random.randn(n_points_per_cluster, 2)]

X = np.r_[X, [-2,3] + .3 * np.random.randn(n_points_per_cluster, 2)]

X = np.r_[X, [3,-2] + 1.6 * np.random.randn(n_points_per_cluster, 2)]

X = np.r_[X, [5,6] + 2 * np.random.randn(n_points_per_cluster, 2)]


#plot scatterplot of points

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(X[:,0], X[:,1], 'b.', ms=2)

plt.savefig('Graph.png', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches=None, pad_inches=0.1)
plt.show()



#run the OPTICS algorithm on the points, using a smoothing value (0 = no smoothing)
RD, CD, order = OP.optics(X,9)
