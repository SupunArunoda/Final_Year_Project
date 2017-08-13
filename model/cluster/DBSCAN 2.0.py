# DBSCAN
# for point in points:
#    if point is visited:
#        continue
#    mark point as visited
#    neighbours = immediate_neighbours(point, epsilon)
#    if len(neighbours) > min_pts:
#        cluster = new_cluster()
#        append point to cluster
#        for n in neighbours:
#            cluster.append(all_neighbours(n))
#    else:
#        mark point as NOISE
#
# def all_neighbours(n, epsilon, cluster):
#     for point in points:
#         if point has not been visited:
#             mark point as visited
#             new_points = immediate_neighbours(point)
#             if len(new_points) > min_pts:
#                 points.append(new_points)
#         if point is not member of any cluster:
#             append point to cluster

from math import pow, sqrt
from pandas import read_csv
import plotly.plotly as py
py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go

class Point(object):
    ''' internal helper class to support algorithm implementation'''

    def __init__(self, feature_vector):
        # feature vector should be something like a list or a numpy
        # array
        self.feature_vector = feature_vector
        self.cluster = None
        self.visited = False

    def __str__(self):
        return str(self.feature_vector)


def _as_points(points):
    ''' convert a list of list- or array-type objects to internal
    Point class'''
    return [Point(point) for point in points]


def as_lists(clusters):
    ''' converts the Points in each cluster back into regular feature
    vectors (lists).'''
    clusters_as_points = {}
    for cluster, members in clusters.items():
        clusters_as_points[cluster] = [member.feature_vector for member in members]
    return clusters_as_points


def print_points(points):
    ''' function for printing lists of points. '''
    s = ''
    for p in points:
        s += str(p) + '\n'
    return s[:-2]


def euclidean(x, y):
    ''' calculate the euclidean distance between x and y.'''
    # sqrt((x0-y0)^2 + ... (xN-yN)^2)
    assert len(x) == len(y)
    sum = 0.0
    for i in range(len(x)):
        sum += pow(x[i] - y[i], 2)
    return sqrt(sum)


def immediate_neighbours(point, all_points, epsilon, distance, debug):
    # use a grid approach it should make this much faster.
    neighbours = []
    for p in all_points:
        if p == point:
            # you cant be your own neighbour...!
            continue
        d = distance(point.feature_vector, p.feature_vector)
        if d < epsilon:
            neighbours.append(p)
    return neighbours


def add_connected(points, all_points, epsilon, min_pts, current_cluster, distance, debug):
    ''' find every point in the set of all_points which are
    density-connected, starting with the initial points list. '''
    cluster_points = []
    for point in points:
        if not point.visited:
            point.visited = True
            new_points = immediate_neighbours(point, all_points, epsilon, distance, debug)
            if len(new_points) >= min_pts:
                # append any new points on the end of the list we're
                # already iterating over.
                for p in new_points:
                    if p not in points:
                        points.append(p)

        # here, we separate 'visited' from cluster membership, since
        # 'visited' only helps keep track of if we've checked this
        # point for neighbours. it may or may not have been assessed
        # for cluster membership at that point.
        if not point.cluster:
            cluster_points.append(point)
            point.cluster = current_cluster
    if debug:
        print('Added points %s' % print_points(cluster_points))
    return cluster_points


def dbscan(points, epsilon, min_pts, distance=euclidean, debug=False):
    ''' Main dbscan algorithm function. pass in a list of feature
    vectors (most likely a list of lists or a list of arrays), a
    radius epsilon within which to search for neighbouring points, and
    a min_pts, the minimum number of neighbours a point must have
    within the radius epsilon to be considered connected. the default
    distance metric is euclidean, but another could be used as
    well. your custom distance metric must accept two equal-length
    feature vectors as input as return a distance value. pass in
    debug=True for verbose output.'''

    assert isinstance(points, list)
    epsilon = float(epsilon)
    if not isinstance(points[0], Point):
        # only check the first list instance. imperfect, but the lists
        # could be arbitrarily long.
        points = _as_points(points)

    if debug:
        print('\nEpsilon: %.2f' % epsilon)
        print('Min_Pts: %d' % min_pts)

    clusters = {}  # each cluster is a list of points
    clusters[-1] = []  # store all the points deemed noise here.
    current_cluster = -1
    for point in points:
        if not point.visited:
            point.visited = True
            neighbours = immediate_neighbours(point, points, epsilon, distance, debug)
            if len(neighbours) >= min_pts:
                current_cluster += 1
                if debug:
                    print('\nCreating new cluster %d' % (current_cluster))
                    print('%s' % str(point))
                point.cluster = current_cluster
                cluster = [point, ]
                cluster.extend(add_connected(neighbours, points, epsilon, min_pts,
                                             current_cluster, distance, debug))
                clusters[current_cluster] = cluster
            else:
                clusters[-1].append(point)
                if debug:
                    print('\nPoint %s has no density-connected neighbours.' % str(point.feature_vector))

    # return the dictionary of clusters, converting the Point objects
    # in the clusters back to regular lists
    return as_lists(clusters)


if __name__ == '__main__':

    import random

    epsilon = 2.0
    min_pts = 2.0
    points = []

    file_path = 'sample.csv'
    datafile = read_csv(file_path)
    datafile = datafile[['time_vector', 'price_vector', 'volume_vector']]
    points = list(datafile.values)
    print(points)

    data = []
    x = []
    y = []
    z = []

    clusters = dbscan(points, epsilon, min_pts, debug=True)
    print('\n========== Results of Clustering =============')
    for cluster, members in clusters.items():
        print('\n--------Cluster %d---------' % cluster)
        for point in members:
            print(point)
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])

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

