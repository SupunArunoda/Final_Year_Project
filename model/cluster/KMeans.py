from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial import distance
import math
import plotly.plotly as py
from scipy.cluster.hierarchy import linkage

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

    for i in range(len(scores)):
        if ((scores[i] > (meanScore - 3 * std_deviation) and scores[i] < (meanScore + 3 * std_deviation))):
            print(i, ': ', scores[i])
        else:
            suspicious.append(i)

    return suspicious


def writeToCSV(data):
    data.to_csv("output/clustered_output_kmeans_ex_type_based_time_framed.csv", index=False, encoding='utf-8')


def plotPlotly(clusters):
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


class Kmeans:
    data = DataFrame()

    def cluster(self, file_path):
        raw_datafile = read_csv(file_path)

        # X = raw_datafile[
        #     ['nom_exe_order_buy_price', 'nom_exe_order_buy_volume', 'nom_exe_order_sell_price',
        #      'nom_exe_order_sell_volume']]
        # X = X.values

        # X = np.array(
        #     [[1.5, 5], [1.7, 6], [1.3, 5.8], [1.3, 5.9], [3.4, 2.6], [3, 2], [3.6, 2.6], [3.1, 2.9], [3, 3], [6.1, 5.5],
        #      [6.3, 5.8], [6.3, 5.7], [6.9, 5.1], [6.4, 5.5]])

        # np.random.seed(4711)  # for repeatability of this tutorial
        # a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100, ])
        # b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50, ])
        # X = np.concatenate((a, b), )

        c = np.random.multivariate_normal([40, 40], [[20, 1], [1, 30]], size=[200, ])
        d = np.random.multivariate_normal([80, 80], [[30, 1], [1, 30]], size=[200, ])
        e = np.random.multivariate_normal([0, 100], [[100, 1], [1, 100]], size=[200, ])
        X = np.concatenate((c, d, e), )

        plt.scatter(X[:, 0], X[:, 1])
        plt.show()

        inertia = []
        for k in range(2, len(X) + 1):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(X)

            inertia.append(kmeans.inertia_)

        print(inertia)

        # last_rev = inertia[::-1]
        idxs = np.arange(1, len(inertia) + 1)
        plt.plot(idxs, inertia)

        acceleration = np.diff(inertia, 2)  # 2nd derivative of the distances
        # acceleration_rev = acceleration[::-1]
        plt.plot(idxs[:-2] + 1, acceleration)
        k = acceleration.argmax() + 2  # if idx 0 is the max of this we want 2 clusters
        print('k: ', k)

        plt.show()

        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)

        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        print(labels)

        clusters = {}
        for i in range(k):
            # select only data observations with cluster label == i
            ds = X[np.where(labels == i)]
            clusters[i] = ds

        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='gist_rainbow')  # plot points with cluster dependent colors
        plt.show()

        # suspicious = calculateScores(clusters, centroids)

        # data = DataFrame(raw_datafile)
        # data['cluster_group'] = np.nan
        # data['anomaly_state'] = np.nan
        #
        # for i in range(len(labels)):
        #     data['cluster_group'].iloc[i] = labels[i]
        #     if labels[i] in suspicious:
        #         data['anomaly_state'].iloc[i] = 'Suspicious'
        #     else:
        #         data['anomaly_state'].iloc[i] = 'Not Suspicious'

        # plotPlotly(clusters)
        # writeToCSV(data)
