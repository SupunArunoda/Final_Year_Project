from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from app.preprocess.dynamic.ExecutionTypeDynamic import ExecutionTypeDynamic
from app.validate.preprocess.OrderbookAttr import OrderbookAttr
from app.validate.preprocess.PriceVolumeAverageTest import PriceVolumeAverage
from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest

from matplotlib import pyplot as plt
from mpld3 import fig_to_html
from flask import Blueprint, request, render_template, redirect, url_for
import sys
from werkzeug.utils import secure_filename
import json

import plotly.plotly as py
py.sign_in('buddhiv', 'YoGay7yhvJSTDCyg0UbP')
import plotly.graph_objs as go
from plotly.offline.offline import _plot_html

preprocess_main = Blueprint('preprocess_main', __name__, template_folder='templates')


# @preprocess_main.route('/preprocess_main', methods=['GET', 'POST'])
@preprocess_main.route('', methods=['GET', 'POST'])
def preprocess_data():
    if (request.method == 'POST'):
        print(request)
        print(request.files)
        print(request.form)
        print(request.stream)
        if ('inputFile' in request.files):
            print('file in request.form')

            file = request.files['inputFile']

            print("ssssssssss")
            print(file)
            print("ssssssssss")

            print(secure_filename(file.filename))

            file.save('./app/data/' + secure_filename(file.filename))

            message_file = './app/data/' + secure_filename(file.filename)
            session_file = './app/data/sessions.csv'

            ex_type_based = ExecutionTypeTest()
            returned_data = ex_type_based.run_execution_type_static(message_file=message_file,
                                                                    session_file=session_file, no_of_lines=0,
                                                                    time_delta=420)

            returned_data['new_orders_percentage'] = round((returned_data['new_orders_count'] / returned_data[
                'total_rows']) * 100, 4)
            returned_data['cancel_orders_percentage'] = round((returned_data['cancel_orders_count'] / returned_data[
                'total_rows']) * 100, 4)
            returned_data['ammend_orders_percentage'] = round((returned_data['ammend_orders_count'] / returned_data[
                'total_rows']) * 100, 4)
            returned_data['execute_orders_percentage'] = round((returned_data['execute_orders_count'] / returned_data[
                'total_rows']) * 100, 4)

            # piechart details
            piechart_labels = ['New Orders', 'Cancelled Orders', 'Ammended Orders', 'Executed Orders']
            piechart_sizes = [returned_data['new_orders_count'], returned_data['cancel_orders_count'],
                              returned_data['ammend_orders_count'], returned_data['execute_orders_count']]

            # test plotly graph
            # labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
            # values = [4500, 2500, 1053, 500]
            # trace = go.Pie(labels=labels, values=values)
            # py.iplot([trace], filename='basic_pie_chart')
            # # trace = [{"x": [1, 2, 3], "y": [3, 1, 6]}]
            # plot_html, plotdivid, width, height = _plot_html(trace, [], "", True, '100%', 525)
            # returned_data['piechart_data'] = plot_html

            returned_data['piechart_labels'] = piechart_labels
            returned_data['piechart_sizes'] = piechart_sizes

        return json.dumps(returned_data)
        # return render_template('preprocess/preprocess.html', data=json.loads(json.dumps(returned_data)))
        # return redirect(url_for('preprocess_route.show_template', data=json.loads(json.dumps(returned_data)), code=307))
        # return json.dumps(request.files)
        # return 'function ok'
