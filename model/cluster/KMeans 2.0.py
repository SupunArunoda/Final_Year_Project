from sklearn.cluster import KMeans
import numpy as np
# from matplotlib import pyplot
import math
from pandas import DataFrame, read_csv
import plotly.plotly as py
py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go

# Retrieve Data
file_path = 'sample.csv'

X = read_csv(file_path)
X = X[['time_vector', 'price_vector', 'volume_vector']]
X = X.values

# X = np.array([[10, 2, 9], [1, 4, 3], [1, 0, 3],
#               [4, 2, 1], [4, 4, 7], [4, 0, 5], [4, 6, 3], [4, 1, 7], [5, 2, 3], [6, 3, 3], [7, 4, 13],[100,200,300]])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

k = int(math.sqrt(len(X) / 2))
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
# # plot the data observations
#     pyplot.plot(ds[:, 0], ds[:, 1], 'o')
#     # plot the centroids
#     lines = pyplot.plot(centroids[i, 0], centroids[i, 1], 'kx')
#     # make the centroid x's bigger
#     pyplot.setp(lines, ms=15.0)
#     pyplot.setp(lines, mew=2.0)
# pyplot.show()

#plot the data using plotly
data = [];
for i in clusters:
    x = []
    y = []
    z = []
    for c in clusters[i]:
        x.append(c[0])
        y.append(c[1])
        z.append(c[2])
    # x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()/
    # print(x,y,z)
    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=6,
            line=dict(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5
            ),
            opacity=0.8
        )
    )
    data.append(trace)

layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='simple-3d-scatter')

# result = zip(X, kmeans.labels_)
# sortedR = sorted(result, key=lambda x: x[1])

print(clusters)

minCluster = 0
minLength = math.inf
for i in clusters:
    if len(clusters[i]) < minLength:
        minCluster = i

for i in clusters[minCluster]:
    print(i)
    print(i[1])
    print(np.float64(0.0011958658638801835))

    # print(abs(i[1] - np.float64(0.0011958658638801835)) < 1e-10)
    # time = abs(i[0] - np.float64(X['time_vector']))

    order = X[(np.float64(X['time_vector']) == i[0]) & (np.float64(X['price_vector']) == i[1]) & (np.float64(X['volume_vector']) == i[2])]

print(order)
