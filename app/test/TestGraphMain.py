from app.model.graph.Histogram import Histogram
from app.model.graph.ScatterPlot import ScatterPlot
from pandas import read_csv

graph_file=read_csv('./../output/window_20/price_gap_regular_19_all.csv')
graph_file_2=read_csv('./../output/window_20/price_gap_regular_18_all.csv')

histogram=Histogram()
histogram.get_two_varaible(datafile_1=graph_file,p1='nom_price_gap',q1='time_index',datafile_2=graph_file_2,p2='nom_price_gap',q2='time_index')

multi_list=[graph_file,'nom_price_gap','time_index',graph_file_2,'nom_price_gap','time_index']

scatterplot=ScatterPlot()
scatterplot.get_two_variable_plot(datafile_1=graph_file,p1='nom_price_gap',q1='time_index',label_1='anomaly',datafile_2=graph_file_2,p2='nom_price_gap',q2='time_index',label_2="non anomaly")