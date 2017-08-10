import numpy as np
import random

from pandas import read_csv
from scipy.spatial import distance
from sklearn.metrics import pairwise_distances
import plotly.plotly as py

py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go


def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape

    if k > n:
        raise Exception('too many medoids')
    # randomly initialize an array of k medoid indices
    M = np.arange(n)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa], C[kappa])], axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]

    # return results
    return M, C


#Plot the result using plotly

file_path = 'sample.csv'
datafile = read_csv(file_path)
datafile = datafile[['time_vector', 'price_vector', 'volume_vector']]
data = list(datafile.values)  # distance matrix
# data = np.array(data)

D = pairwise_distances(data, metric='euclidean')

num_clusters = k = int(np.math.sqrt(len(data) / 2))
# split into num_clusters clusters
M, C = kMedoids(D, num_clusters)

print('medoids:')
for point_idx in M:
    print(data[point_idx])

plotData = []


print('')
print('clustering result:')
clusters = {}
for label in C:
    temp = []
    print('cluster', label, ': ')

    x = []
    y = []
    z = []
    for point_idx in C[label]:
        x.append(data[point_idx][0])
        y.append(data[point_idx][1])
        z.append(data[point_idx][2])

        temp.append(data[point_idx])
        # print('label {0}:　{1}'.format(label, data[point_idx]))
        print(data[point_idx])
    print('')
    clusters[label] = temp

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
    plotData.append(trace)

layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
fig = go.Figure(data=plotData, layout=layout)
py.iplot(fig, filename='simple-3d-scatter')

#Find the suspicious clusters

scores = []
for i in clusters:
    # if len(clusters[i]) < minLength:
    #     minCluster = i
    tempClusters = list(clusters.keys())
    tempClusters = tempClusters[0:i] + tempClusters[i + 1:]

    distTotal = 0
    for j in tempClusters:
        dist = distance.euclidean(M[i], M[j])
        distTotal += dist
    distMean = distTotal / len(tempClusters)
    scores.append(distMean / len(clusters[i]))

print(scores)

print(scores.index(max(scores)))
print(clusters[scores.index(max(scores))])
