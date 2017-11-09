from app.module.momentum_ignition.MomentumIgnition import MomentumIgnition
from app.db.PreprocessFileController import PreprocessFileController
from app.db.PreprocessFile import PreprocessFile
from time import gmtime, strftime
import sys
momentumIgnition = MomentumIgnition()
momentumIgnition.analyze(file_path='../output/entropy.csv')
# uploaded_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# pfc=PreprocessFileController()
# last_process_end = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# last_process_start = strftime("%Y-%m-%d %H:%M:%S", gmtime())
# input_file='./app/data/data.csv'
# output_file='./app/data/out.csv'
# pf = PreprocessFile(input_file=input_file, uploaded_time=uploaded_time, last_process_start=last_process_start,
#                             last_process_end=last_process_end, output_file=output_file)
#
# val = pfc.saveProcessFile(pf)
# print(val)

a = [4, 8, 0, 1, 5]

m = min(i for i in a if i > 0)
print(m)
min_val=sys.maxsize
print(min_val)