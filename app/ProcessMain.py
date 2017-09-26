from pandas import read_csv
import json, fnmatch, os
from flask import Blueprint, request

import numpy as np
from scipy.signal import argrelextrema

process_main = Blueprint('process_main', __name__, template_folder='templates')


@process_main.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        id = data['id']

        max_anomalous_file = 12

        fileslist = fnmatch.filter(os.listdir('app/output/'), str(id) + '_price_gap_regular_*.csv')

        return_data = {}
        return_data['files_count'] = len(fileslist)
        return_data['max_anomalous_file'] = max_anomalous_file

        read_messages = read_csv('app/output/' + str(id) + '_entropy_20.csv', header=None)
        read_messages.columns = ['entropy_exec_type', 'entropy_side', 'time_index']
        data = read_messages

        return_data['entropy_exec_type'] = list(data['entropy_exec_type'])[1:]
        return_data['time_index'] = list(data['time_index'])[1:]

        x = data.values[:, 0][1:]
        x = [float(i) for i in x]
        x = np.array(x)
        local_minimas = argrelextrema(x, np.less)
        local_minimas = np.array(local_minimas).tolist()[0]

        return_data['local_minimas'] = local_minimas

        return json.dumps(return_data)


@process_main.route('/select_data', methods=['GET', 'POST'])
def select_data():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        id = data['id']
        file_number = data['file_number']

        read_messages = read_csv('app/output/' + str(id) + '_price_gap_regular_' + str(file_number) + '_all.csv',
                                 header=None)
        read_messages.columns = ['price_gap', 'time_index', 'nom_price_gap']
        data = read_messages

        return_data = {}

        return_data['price_gap'] = list(data['price_gap'])[1:]
        return_data['time_index'] = list(data['time_index'])[1:]
        return_data['nom_price_gap'] = list(data['nom_price_gap'])[1:]

        return json.dumps(return_data);
