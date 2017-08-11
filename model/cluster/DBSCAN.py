import numpy as np
from pandas import DataFrame, read_csv
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


##############################################################################
# # Generate sample data
# centers = [[1, 1], [-1, -1], [1, -1]]
# datafile, labels_true = make_blobs(n_samples=150, centers=centers, cluster_std=0.4,
#                             random_state=0)
#
# datafile = StandardScaler().fit_transform(datafile)
#
# print(datafile)

##############################################################################
# Retrieve Data

file_path = 'sample.csv'
datafile = read_csv(file_path)
# datafile.drop(['Best_Bid_Ask','Direction','Order_ID','Price','Volume','mult','Execution_Time'],axis = 1,inplace = True)
datafile = datafile[['time_vector','price_vector','volume_vector']]
print(datafile.values)


##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(datafile)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# print('Estimated number of clusters: %d' % n_clusters_)
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# print("Adjusted Rand Index: %0.3f"
#       % metrics.adjusted_rand_score(labels_true, labels))
# print("Adjusted Mutual Information: %0.3f"
#       % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

##############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = datafile[class_member_mask & core_samples_mask]
    print(class_member_mask & core_samples_mask)

    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)
    # print(xy.iloc[:, 0])

    xy = datafile[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
