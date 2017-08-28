from matplotlib import pyplot as plt
from pandas import read_csv
import numpy as np



raw_datafile = read_csv('../../output/analyzing values/price_gap_buy_anomaly.csv')
X = raw_datafile[['nom_buy_price_gap', 'time_index']]
X = X.values
x = X[:, 0]
y = np.array(range(1, len(X)+1))
plt.plot(y, x)
plt.show()
#
# count=1
# for i in range(26):
#     if(i!=0):
#         raw_datafile = read_csv('../../output/price_gap_regular_'+str(i)+'_all.csv')
# #raw_datafile_best_buy = read_csv('../../output/analyzing values/price_gap_sell_norm_10_50.csv')
#
#         X = raw_datafile[['nom_price_gap', 'time_index']]
#         X = X.values
# # Y = raw_datafile_best_buy[['nom_sell_price_gap', 'time_index']]
# # Y = Y.values
#
#         x = X[:, 0]
#         y = np.array(range(1, len(X)+1))
#         plt.plot(y, x)
#         plt.show()
#         print(i)

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




