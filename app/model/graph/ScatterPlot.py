from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np

class ScatterPlot:

    def get_one_variable(self,datafile,p,q):
        X = datafile[[p, q]]
        X = X.values

        x = X[:, 0]
        y = np.array(range(1, len(X) + 1))
        plt.scatter(y, x,alpha=1)
        plt.show()

    def get_two_variable_plot(self,datafile_1,p1,q1,label_1,datafile_2,p2,q2,label_2):
        X = datafile_1[[p1, q1]]
        X = X.values

        x = X[:, 0]
        y = np.array(range(1, len(X) + 1))
        plt.scatter(y, x, alpha=1,label=label_1)
        #plt.show()

        Y = datafile_2[[p2, q2]]
        Y = Y.values

        x = Y[:, 0]
        y = np.array(range(1, len(Y) + 1))
        plt.scatter(y, x, alpha=1,label=label_2)
        plt.show()
