from pandas import read_csv, DataFrame
import json, fnmatch, os
from flask import Blueprint, request
import sys

import numpy as np
from scipy.signal import argrelextrema

process_main = Blueprint('process_main', __name__, template_folder='templates')


@process_main.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        id = data['id']

        fileslist = fnmatch.filter(os.listdir('app/output/'), str(id) + '_price_gap_regular_*.csv')

        return_data = {}
        return_data['files_count'] = len(fileslist)

        read_messages = read_csv('app/output/' + str(id) + '_entropy.csv', header=None)
        read_messages.columns = ['entropy_exec_type', 'entropy_side', 'time_index']
        data = read_messages

        return_data['entropy_exec_type'] = list(data['entropy_exec_type'])[1:]
        return_data['time_index'] = list(data['time_index'])[1:]

        x = data.values[:, 0][1:]
        x = [float(i) for i in x]
        x = np.array(x)
        local_minimas = argrelextrema(x, np.less)
        local_minimas = np.array(local_minimas).tolist()[0]

        max_anomalous_file = sys.maxsize
        for i in local_minimas:
            val = float(data['entropy_exec_type'].iloc[i])
            if (val < max_anomalous_file):
                max_anomalous_file = val
                data_point = i
        print("file", data_point + 1)
        return_data['max_anomalous_file'] = data_point + 1

        # m = min(i for i in local_minimas if i > 0)

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
        read_messages.columns = ['end_broker', 'price_gap', 'start_broker', 'time_index', 'nom_price_gap']
        data = read_messages

        price_gap_data = {}

        price_gap_data['price_gap'] = list(data['price_gap'])[1:]
        price_gap_data['time_index'] = list(data['time_index'])[1:]
        price_gap_data['nom_price_gap'] = list(data['nom_price_gap'])[1:]
        price_gap_data['end_broker'] = list(data['end_broker'])[1:]
        price_gap_data['start_broker'] = list(data['start_broker'])[1:]
        return_data = {}
        return_data['price_gap_data'] = price_gap_data

        f = 'app/output/orderbook_simulation_' + str(file_number) + '.csv'
        if (os.path.exists(f)):
            read_messages = read_csv(f, header=None)
            read_messages.columns = ['best_ask', 'best_bid', 'time_index', 'top_buy_price_points',
                                     'top_sell_price_points']
            orderbook_data = read_messages.values[1:].tolist()
        else:
            orderbook_data = None

        return_data['orderbook_data'] = orderbook_data

        return json.dumps(return_data)


@process_main.route('/get_broker_data', methods=['GET', 'POST'])
def get_broker_data():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        broker_id = data['broker_id']
        current_file = data['file_id']
        id = data['id']

        dataframe = read_csv('./app/output/' + str(id) + '_all_attributes_' + str(current_file) + '.csv')

        data = dataframe.loc[dataframe['broker_id'] == broker_id]

        return_data = {}
        return_data['order_count'] = len(data)

        return_data['orders'] = data.values[:].tolist()

        order_types = {}
        order_types['new'] = data.loc[data['execution_type'] == 0].values[:].tolist()
        order_types['cancel'] = data.loc[data['execution_type'] == 4].values[:].tolist()
        order_types['ammend'] = data.loc[data['execution_type'] == 5].values[:].tolist()
        order_types['execute'] = data.loc[data['execution_type'] == 15].values[:].tolist()

        order_types_count = {}
        order_types_count['new'] = len(order_types['new'])
        order_types_count['cancel'] = len(order_types['cancel'])
        order_types_count['ammend'] = len(order_types['ammend'])
        order_types_count['execute'] = len(order_types['execute'])

        return_data['order_types'] = order_types
        return_data['order_types_count'] = order_types_count

        return json.dumps(return_data)


@process_main.route('/get_timeframe_data', methods=['GET', 'POST'])
def get_timeframe_data():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        id = data['id']
        file_number = data['file_id']

        read_messages = read_csv('app/output/' + str(id) + '_all_attributes_' + str(file_number) + '.csv',
                                 header=None)
        read_messages.columns = ['broker_id', 'executed_qty', 'executed_value', 'execution_type', 'instrument_id',
                                 'order_id', 'order_qty', 'side', 'total_qty', 'transact_time', 'value', 'visible_size']

        data = read_messages

        return_data = {}
        allOrder = []
        newOrder = []
        ammendOrder = []
        cancelOrder = []
        executedOrder = []
        broker_details = DataFrame()

        return_data['new'] = len(data.loc[(data['execution_type'] == '0') | (data['execution_type'] == 0)].values[:].tolist())
        return_data['cancel'] = len(data.loc[(data['execution_type'] == '4')  | (data['execution_type'] == 4)].values[:].tolist())
        return_data['ammend'] = len(data.loc[(data['execution_type'] == '5')  | (data['execution_type'] == 5)].values[:].tolist())
        return_data['execute'] = len(data.loc[(data['execution_type'] == '15')  | (data['execution_type'] == 15)].values[:].tolist())
        return_data['all'] = return_data['new'] + return_data['cancel'] + return_data['ammend']+ return_data['execute']

        brokers = data['broker_id'].unique()

        for i in range(1,len(brokers)):
            temp = DataFrame(data.loc[data['broker_id'] == brokers[i]].values[:])
            allOrder.append(len(temp))
            newOrder.append(len(temp.loc[temp[3] == 0].values[:].tolist()))
            cancelOrder.append(len(temp.loc[temp[3] == 4].values[:].tolist()))
            ammendOrder.append(len(temp.loc[temp[3] == 5].values[:].tolist()))
            executedOrder.append(len(temp.loc[temp[3] == 15].values[:].tolist()))

        broker_details['broker_id'] = brokers.tolist()[1:]
        broker_details['all'] = allOrder
        broker_details['new'] = newOrder
        broker_details['cancel'] = cancelOrder
        broker_details['ammend'] = ammendOrder
        broker_details['execute'] = executedOrder

        sortedNew = broker_details.sort_values(['new'],  ascending=[False])
        sortedCancel = broker_details.sort_values(['cancel'], ascending=[False])
        sortedAmmend = broker_details.sort_values(['ammend'], ascending=[False])
        sortedExecute = broker_details.sort_values(['execute'], ascending=[False])
        sortedAll = broker_details.sort_values(['all'], ascending=[False])

        return_data['sortedNew'] = list(sortedNew['broker_id'])
        return_data['sortedCancel'] = list(sortedCancel['broker_id'])
        return_data['sortedAmmend'] = list(sortedAmmend['broker_id'])
        return_data['sortedExecute'] = list(sortedExecute['broker_id'])
        return_data['sortedAll'] = list(sortedAll['broker_id'])

        return json.dumps(return_data)