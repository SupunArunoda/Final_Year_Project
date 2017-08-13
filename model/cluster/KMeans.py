from sklearn.cluster import KMeans
import numpy as np
from scipy.spatial import distance
import math
import plotly.plotly as py

py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go
from pandas import DataFrame


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
    # print(scores)
    std_deviation = np.std(scores)
    meanScore = np.mean(scores)
    print(meanScore, ' .... ', std_deviation)

    for i in range(len(scores)):
        if ((scores[i] > abs(meanScore - 3 * std_deviation) or scores[i] > abs(meanScore + 3 * std_deviation))):
            print(i, ': ', scores[i])
            suspicious.append(i)
    return suspicious


def writeToCSV(data):
    data.to_csv("output/clustered_output_kmeans.csv", index=False, encoding='utf-8')


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


class Kmeans:
    data = DataFrame()

    def cluster(raw_datafile):
        X = raw_datafile[
            ['cancel_order_buy', 'cancel_order_sell', 'execute_order_buy', 'execute_order_sell', 'new_order_buy',
             'new_order_sell']]
        X = X.values
        data = DataFrame(raw_datafile)
        k = int(math.sqrt(len(X) / 2))

        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)

        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        clusters = {}
        data['cluster_group'] = np.nan
        data['anomaly_state'] = np.nan

        for i in range(k):
            # select only data observations with cluster label == i
            ds = X[np.where(labels == i)]
            clusters[i] = ds

        suspicious = calculateScores(clusters, centroids)

        for i in range(len(labels)):
            data['cluster_group'].iloc[i] = labels[i]
            if labels[i] in suspicious:
                data['anomaly_state'].iloc[i] = 'Suspicious'
            else:
                data['anomaly_state'].iloc[i] = 'Not Suspicious'

        writeToCSV(data)
