from docutils.nodes import target

from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from app.preprocess.static.OrderbookSimulation import OrderbookSimulation
from app.preprocess.window.EventWindow import EventWindow
from app.preprocess.window.TimeWindow import TimeWindow
from app.preprocess.static.OrderbookSimulation import OrderbookSimulation

from app.validate.preprocess.OrderbookAttr import OrderbookAttr

from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest
from app.validate.preprocess.AllAttributes import AllAttribute

from pandas import read_csv
from matplotlib import pyplot as plt
from flask import Blueprint, request, render_template, redirect, url_for
import sys
from werkzeug.utils import secure_filename
import json
from threading import Thread

# import plotly.plotly as py

# py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go
from plotly.offline.offline import _plot_html

from app.validate.preprocess.OrderbookSimulationTest import OrderbookSimulationTest

preprocess_main = Blueprint('preprocess_main', __name__, template_folder='templates')


def orderbook_thread(message_file, session_file,size,type):
    order_sim = OrderbookSimulationTest()
    if (type == "time"):
        order_book_window = TimeWindow(time_delta=size)
    else:
        order_book_window = EventWindow(no_of_events=size)
    order_sim.run_orderbook_simulation(message_file=message_file, session_file=session_file,
                                       window=order_book_window)


@preprocess_main.route('/process', methods=['GET', 'POST'])
def process():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))

        message_file = './app/data/' + data['file_name']
        session_file = './app/data/sessions.csv'

        message_dataframe = read_csv(message_file)
        print(message_dataframe.columns)
        # message_dataframe.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time','execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size','order_id']
        session_dataframe = read_csv(session_file, header=None)
        print(session_dataframe.columns)
        session_dataframe.columns = ['instrument_id', 'transact_time', 'session_status', 'session_name',
                                     'order_book_id']

        window_type = data['type']
        window_size = int(data['window'])
        is_order_book=data['orderbook_simulation']

        if (window_type == 'time'):
            window_size = window_size * 60
        elif (window_type == 'order'):
            window_size = window_size

        print(data['orderbook_simulation'])
        print(type(data['orderbook_simulation']))

        if (data['orderbook_simulation'] == True):
            Thread(target=orderbook_thread, args=[message_file, session_file,window_size,window_type])

        all_attributes = AllAttribute()
        return_data = all_attributes.run(message_file=message_dataframe, session_file=session_dataframe, type=window_type,
                                   size=window_size,is_order_book=is_order_book)

        # return_data= 3
        return json.dumps(return_data)


@preprocess_main.route('/set_session_information', methods=['GET', 'POST'])
def set_session_information():
    if (request.method == 'POST'):
        if ('sessionsFile' in request.files):
            file = request.files['sessionsFile']

            print(secure_filename(file.filename))

            file.save('./app/data/sessions.csv')
            file_path = './app/data/sessions.csv'

            read_session = read_csv(file_path, header=None)
            print(read_session)
            read_session.columns = ['instrument_id', 'transact_time', 'session_status', 'session_name',
                                    'order_book_id']
            data = read_session

            sessions = data.values[1:]

            return_data = {}
            return_data['instrument_id'] = sessions[0][0]
            return_data['session_date'] = sessions[0][1].split(' ')[0]

            session_data = []
            for i in range(0, len(sessions), 2):
                # session_duration =
                session_data.append([sessions[i][3], sessions[i][1], sessions[i + 1][1]])

            return_data['session_data'] = session_data
            # return_data['session_datas'] = sessions.tolist()

            return json.dumps(return_data)
            # return 'done'


@preprocess_main.route('/get_csv_information', methods=['GET', 'POST'])
def get_csv_information():
    if (request.method == 'POST'):
        if ('inputFile' in request.files):
            file = request.files['inputFile']

            print(secure_filename(file.filename))

            file.save('./app/data/' + secure_filename(file.filename))
            file_path = './app/data/' + secure_filename(file.filename)

            print(file_path)

            read_messages = read_csv(file_path)
            # read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
            #                          'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
            #                          'order_id']
            data = read_messages

            return_data = {}
            return_data['new_orders_count'] = 0
            return_data['ammend_orders_count'] = 0
            return_data['cancel_orders_count'] = 0
            return_data['execute_orders_count'] = 0
            return_data['total_rows'] = len(data)

            for index, order_row in data.iterrows():
                if order_row['execution_type'] == 0:
                    return_data['new_orders_count'] = return_data['new_orders_count'] + 1
                if order_row['execution_type'] == 4:
                    return_data['cancel_orders_count'] = return_data['cancel_orders_count'] + 1
                if order_row['execution_type'] == 5:
                    return_data['ammend_orders_count'] = return_data['ammend_orders_count'] + 1
                if order_row['execution_type'] == 15:
                    return_data['execute_orders_count'] = return_data['execute_orders_count'] + 1

            return_data['new_orders_percentage'] = round((return_data['new_orders_count'] / return_data[
                'total_rows']) * 100, 4)
            return_data['cancel_orders_percentage'] = round((return_data['cancel_orders_count'] / return_data[
                'total_rows']) * 100, 4)
            return_data['ammend_orders_percentage'] = round((return_data['ammend_orders_count'] / return_data[
                'total_rows']) * 100, 4)
            return_data['execute_orders_percentage'] = round((return_data['execute_orders_count'] / return_data[
                'total_rows']) * 100, 4)

            # piechart details
            piechart_labels = ['New Orders', 'Cancelled Orders', 'Ammended Orders', 'Executed Orders']
            piechart_sizes = [return_data['new_orders_count'], return_data['cancel_orders_count'],
                              return_data['ammend_orders_count'], return_data['execute_orders_count']]

            return_data['piechart_labels'] = piechart_labels
            return_data['piechart_sizes'] = piechart_sizes
            return json.dumps(return_data)
