from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

from scipy.cluster.hierarchy import fcluster


class Hierarchical:
    def cluster(self, data, distance_method):
        X = data

        Z = linkage(X, distance_method)
        c, coph_dists = cophenet(Z, pdist(X))

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

        last = Z[:, 2]
        last_rev = last[::-1]
        idxs = np.arange(1, len(last) + 1)
        plt.plot(idxs, last_rev)

        acceleration = np.diff(last, 2)  # 2nd derivative of the distances
        acceleration_rev = acceleration[::-1]
        plt.plot(idxs[:-2] + 1, acceleration_rev)
        k = acceleration_rev.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
        print("clusters:", k)

        max_d = last_rev[k - 2]
        print('max_d: ', max_d)

        plt.show()

        fancy_dendrogram(
            Z,
            leaf_rotation=90.,
            leaf_font_size=12.,
            show_contracted=True,
            annotate_above=10,  # useful in small plots so annotations don't overlap
            max_d=max_d,
        )
        plt.show()

        cluster_data = fcluster(Z, k, criterion='maxclust')

        clusters = {}
        for i in range(1, k + 1):
            # select only data observations with cluster label == i
            ds = X[np.where(cluster_data == i)]
            clusters[i] = ds

            print('cluster ', i, ds)

        return clusters;