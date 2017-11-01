from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from app.preprocess.window.EventWindow import EventWindow
from app.preprocess.window.TimeWindow import TimeWindow

from app.validate.preprocess.OrderbookAttr import OrderbookAttr

from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest

from pandas import read_csv
from matplotlib import pyplot as plt
from flask import Blueprint, request, render_template, redirect, url_for
import sys
from werkzeug.utils import secure_filename
import json

# import plotly.plotly as py

# py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go
from plotly.offline.offline import _plot_html

preprocess_main = Blueprint('preprocess_main', __name__, template_folder='templates')


@preprocess_main.route('/process', methods=['GET', 'POST'])
def process():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))

        message_file = './app/data/' + data['file_name']
        session_file = './app/data/sessions.csv'

        window_type = data['type']
        window_size = data['window']

        if(window_type=='time'):
            window= TimeWindow(time_delta=window_size)
        else:
            window= EventWindow(no_of_events=window_size)

        ex_type_based = ExecutionTypeTest()
        index = ex_type_based.run_execution_type_static(message_file=message_file,
                                                        session_file=session_file, no_of_lines=0,
                                                        time_delta=420, window=window)

        return str(index)


@preprocess_main.route('/get_csv_information', methods=['GET', 'POST'])
def get_csv_information():
    if (request.method == 'POST'):
        if ('inputFile' in request.files):
            file = request.files['inputFile']

            print(secure_filename(file.filename))

            file.save('./app/data/' + secure_filename(file.filename))
            file_path = './app/data/' + secure_filename(file.filename)

            print(file_path)

            read_messages = read_csv(file_path, header=None)
            read_messages.columns = ['instrument_id', 'broker_id', 'executed_value', 'value', 'transact_time',
                                     'execution_type', 'order_qty', 'executed_qty', 'total_qty', 'side', 'visible_size',
                                     'order_id']
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
