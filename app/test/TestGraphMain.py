from app.model.graph.Histogram import Histogram
from app.model.graph.ScatterPlot import ScatterPlot
from pandas import read_csv

graph_file=read_csv('./../output/window_20/price_gap_regular_19_all.csv')
graph_file_2=read_csv('./../output/window_20/price_gap_regular_18_all.csv')
entropy_file_5=read_csv('./../output/entropy/entropy_5mins.csv')
entropy_file_5_15=read_csv('./../output/entropy/entropy_5_15mins.csv')
entropy_file_6=read_csv('./../output/entropy/entropy_6mins.csv')
entropy_file_7=read_csv('./../output/entropy/entropy_7mins.csv')
entropy_file_10=read_csv('./../output/entropy/entropy_10mins.csv')
entropy_file_15=read_csv('./../output/entropy/entropy_15mins.csv')
entropy_file_20=read_csv('./../output/entropy/entropy_20.csv')



histogram=Histogram()
#histogram.get_two_varaible(datafile_1=graph_file,p1='nom_price_gap',q1='time_index',datafile_2=graph_file_2,p2='nom_price_gap',q2='time_index')

# count=1
# for i in range(26):
#      if(i!=0):
#          print(i)
#          raw_datafile = read_csv('./../output/price_gap_regular_'+str(i)+'_all.csv')
#          histogram.get_one_variable(datafile=raw_datafile,p='nom_price_gap',q='time_index')
         #histogram.get_two_varaible(datafile_1=raw_datafile, p1='nom_price_gap', q1='time_index', datafile_2=raw_datafile,p2='std_price_gap', q2='time_index')

#multi_list=[graph_file,'nom_price_gap','time_index',graph_file_2,'nom_price_gap','time_index']

# scatterplot=ScatterPlot()
#scatterplot.get_two_variable_plot(datafile_1=graph_file,p1='nom_price_gap',q1='time_index',label_1='anomaly',datafile_2=graph_file_2,p2='nom_price_gap',q2='time_index',label_2="non anomaly")
histogram.get_one_variable(datafile=entropy_file_5,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_5_15,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_6,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_7,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_10,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_15,p='entropy_exec_type',q='time_index')
histogram.get_one_variable(datafile=entropy_file_20,p='entropy_exec_type',q='time_index')