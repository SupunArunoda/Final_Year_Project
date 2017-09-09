from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np
from scipy import fft

class Histogram:

    def get_one_variable_fft(self,datafile,p,q):
        X = datafile[[p, q]]
        X = X.values

        x = X[:, 0]
        y = np.array(range(1, len(X) + 1))
        x=fft(x)
        plt.plot(y, x)
        plt.show()

    def get_one_variable(self,datafile,p,q):
        X = datafile[[p, q]]
        X = X.values

        x = X[:, 0]
        y = np.array(range(1, len(X) + 1))
        plt.plot(y, x)
        plt.show()

    def get_two_varaible(self,datafile_1,p1,q1,datafile_2,p2,q2):
        X = datafile_1[[p1, q1]]
        X = X.values
        x = X[:, 0]
        y = np.array(range(1, len(X)+1))
        plt.plot(y, x)
        #plt.show()

        Y = datafile_2[[p2, q2]]
        Y = Y.values

        x = Y[:, 0]
        y = np.array(range(1, len(Y)+1))
        plt.plot(y, x)
        plt.show()


# raw_datafile = read_csv('../../output/real/ex_type_norm_10.0.csv')
# X = raw_datafile[['nom_exe', 'time_index_volume']]
# X = X.values
# x = X[:, 0]
# y = np.array(range(1, len(X)+1))
# plt.plot(y, x)
# plt.show()
# #

# count=1
# for i in range(26):
#     if(i!=0):
#         raw_datafile = read_csv('./app/output/price_gap_regular_'+str(i)+'_all.csv')
# # #raw_datafile_best_buy = read_csv('../../output/analyzing values/price_gap_sell_norm_10_50.csv')
# #
#         X = raw_datafile[['price_gap', 'time_index']]
#         X = X.values
#
#         x = X[:, 0]
#         y = np.array(range(1, len(X)+1))
#         plt.plot(y, x)
#         plt.show()
#         print(i)


# raw_datafile_best_buy = read_csv('F:/Acadamic/Final Year Research/Project/Final_Year_Project/app/output/price_gap_buy_anomaly.csv')
# Y = raw_datafile_best_buy[['nom_buy_price_gap', 'time_index']]
# Y = Y.values
#
# x = Y[:, 0]
# y = np.array(range(1, len(Y)+1))
# plt.plot(y, x)
# plt.show()


# create some data to use for the plot
# dt = 0.1
# t = np.arange(0.0, 20.0, dt)
# r = np.exp(-t[:10] / 0.05)  # impulse response
#
# x = np.random.randn(len(t))
# s = np.convolve(x, r)[:len(x)] * dt  # colored noise
#
# print(t)
# print(s)
# print(len(t))
# print(len(s))

# the main axes is subplot(111) by default
# plt.plot(y, x)
# plt.axis([0, 1, 1.1 * np.min(x), 2 * np.max(x)])
# plt.xlabel('time (s)')
# plt.ylabel('current (nA)')
# plt.title('Gaussian colored noise')




