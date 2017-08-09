from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot
import math
from pandas import DataFrame, read_csv

#Retrieve Data
file_path = 'sample.csv'

X = read_csv(file_path)
X = X[['time_vector','price_vector','volume_vector']]
X = X.values

# X = np.array([[10, 2, 9], [1, 4, 3], [1, 0, 3],
#               [4, 2, 1], [4, 4, 7], [4, 0, 5], [4, 6, 3], [4, 1, 7], [5, 2, 3], [6, 3, 3], [7, 4, 13],[100,200,300]])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

k = int(math.sqrt(len(X)/2))
# k = 3
kmeans = KMeans(n_clusters=k)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_
clusters = {}

for i in range(k):
    # select only data observations with cluster label == i
    ds = X[np.where(labels == i)]

    clusters[i] = ds
    # plot the data observations
    pyplot.plot(ds[:, 0], ds[:, 1], 'o')
    # plot the centroids
    lines = pyplot.plot(centroids[i, 0], centroids[i, 1], 'kx')
    # make the centroid x's bigger
    pyplot.setp(lines, ms=15.0)
    pyplot.setp(lines, mew=2.0)
pyplot.show()

result = zip(X, kmeans.labels_)

sortedR = sorted(result, key=lambda x: x[1])
print(clusters)
