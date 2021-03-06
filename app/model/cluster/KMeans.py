from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial import distance
import plotly.plotly as py

# py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go
from pandas import DataFrame, read_csv
from matplotlib import pyplot as plt


def calculateScores(clusters, centroids):
    scores = []
    suspicious = []
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
    std_deviation = np.std(scores)
    meanScore = np.mean(scores)
    # print(meanScore, ' .... ', std_deviation)

    # for i in range(len(scores)):
    #     if ((scores[i] > (meanScore - 3 * std_deviation) and scores[i] < (meanScore + 3 * std_deviation))):
    #         print(i, ': ', scores[i])
    #     else:
    #         suspicious.append(i)

    return scores


def plotPlotly(clusters):
    # plot the data using plotly
    data = []
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


class Kmeans:
    def cluster(self, data):
        X = data
        print(len(X))
        inertia = []
        for k in range(2, len(X) + 1):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(X)

            inertia.append(kmeans.inertia_)

        # print(inertia)

        # last_rev = inertia[::-1]
        idxs = np.arange(1, len(inertia) + 1)
        # plt.plot(idxs, inertia)

        acceleration = np.diff(inertia, 2)  # 2nd derivative of the distances
        # acceleration_rev = acceleration[::-1]
        # plt.plot(idxs[:-2] + 1, acceleration)
        k = acceleration.argmax() + 3  # if idx 0 is the max of this we want 2 clusters
        print('k: ', k)

        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)

        labels = kmeans.labels_

        print(labels)

        clusters = {}
        for i in range(k):
            # select only data observations with cluster label == i
            ds = X[labels == i]
            clusters[i] = ds

        return [clusters, kmeans]

    def writeToCSV(self, clusters, kmeans, raw_datafile):
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        scores = calculateScores(clusters, centroids)

        data = DataFrame(raw_datafile)
        data['cluster_group'] = np.nan
        data['index'] = np.nan
        data['anomaly_score'] = np.nan
        # data['anomaly_state'] = np.nan

        for i in range(len(labels)):
            data['cluster_group'].iloc[i] = labels[i]

            for j in range(len(scores)):
                if labels[i] == j:
                    data['index'] = j
                    data['anomaly_score'].iloc[i] = scores[j]

        # data.to_csv("../output/clustered_output.csv", index=False, encoding='utf-8')
        print(data)
        return data[['index','anomaly_score']]
