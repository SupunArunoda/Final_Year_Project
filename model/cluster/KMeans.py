from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial import distance
import math
import plotly.plotly as py
py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go

# kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

class Kmeans:
    def cluster(X):
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

        scores = []
        for i in clusters:

            tempClusters = list(clusters.keys())
            tempClusters = tempClusters[0:i] + tempClusters[i + 1:]

            distTotal = 0
            for j in tempClusters:
                dist = distance.euclidean(centroids[i], centroids[j])
                distTotal += dist
            distMean = distTotal / len(tempClusters)
            scores.append(distMean / len(clusters[i]))
        print(scores)
        print(clusters[scores.index(max(scores))])

    def plot(clusters):
        # plot the data using plotly
        data = [];
        for i in clusters:
            x = []
            y = []
            z = []
            for c in clusters[i]:
                x.append(c[0])
                y.append(c[1])
                z.append(c[2])

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

