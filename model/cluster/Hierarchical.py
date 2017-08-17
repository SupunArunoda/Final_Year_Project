from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

from scipy.cluster.hierarchy import inconsistent
from scipy.cluster.hierarchy import fcluster

from pandas import read_csv, DataFrame

# np.random.seed(4711)  # for repeatability of this tutorial
# a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100, ])
# b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50, ])
# X = np.concatenate((a, b), )
# print(type(X))

# X = np.array([[2,3],[5,4],[1,2],[3,2],[4,4],[7,6],[1,6],[5,6],[3,3],[5,3]])
# print(type(X))

raw_datafile = read_csv('E:\Academic\Semester 6B\FYP\Project01\FinalYearProject02\output\price_volume_average_time_framed_data.csv')
X = raw_datafile[['execute_order_buy_price', 'execute_order_buy_volume', 'execute_order_sell_price', 'execute_order_sell_volume']]  # X = raw_datafile.drop('time_index_volume', 1)
# X = raw_datafile.drop(raw_datafile.columns[[1, 3, 7, 11, 12]], axis=1)
X = X.values
print(X)
data = DataFrame(raw_datafile)

print(X)  # 150 samples with 2 dimensions
print(X.shape)  # 150 samples with 2 dimensions
plt.scatter(X[:, 0], X[:, 1])
plt.show()

Z = linkage(X, "ward")
c, coph_dists = cophenet(Z, pdist(X))

print(Z)


def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata


# Calculate the Dendogram
# plt.figure(figsize=(25, 10))

# fancy_dendrogram(
#     Z,
#     truncate_mode='lastp',
#     p=12,
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,
#     annotate_above=10,  # useful in small plots so annotations don't overlap
# )
# plt.show()

# depth = 3
# incons = inconsistent(Z, depth)
# incons[-10:]

last = Z[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
# plt.plot(idxs, last_rev)

acceleration = np.diff(last, 2)  # 2nd derivative of the distances
acceleration_rev = acceleration[::-1]
# plt.plot(idxs[:-2] + 1, acceleration_rev)
k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
print("clusters:", k)

clusters = fcluster(Z, k, criterion='maxclust')

plt.figure(figsize=(10, 8))
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
plt.show()
