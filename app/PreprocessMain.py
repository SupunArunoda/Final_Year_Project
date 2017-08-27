from app.orderbook.Order import Order
from app.orderbook.OrderBook import OrderBook
from app.preprocess.dynamic.ExecutionTypeDynamic import ExecutionTypeDynamic
from app.validate.preprocess.OrderbookAttr import OrderbookAttr
from app.validate.preprocess.PriceVolumeAverageTest import PriceVolumeAverage
from app.validate.preprocess.ExecutionTypeTest import ExecutionTypeTest

import pandas as pd

# from app.validate.model.Kmeans import KMeans

from flask import Blueprint, request, render_template, redirect, url_for
import sys
from werkzeug.utils import secure_filename
import json

preprocess_main = Blueprint('preprocess_main', __name__, template_folder='templates')


@preprocess_main.route('/preprocess_main', methods=['GET', 'POST'])
@preprocess_main.route('/', methods=['GET', 'POST'])
def preprocess_data():
    if (request.method == 'POST'):
        if ('inputFile' in request.files):
            file = request.files['inputFile']
            file.save('./app/data/' + secure_filename(file.filename))

            message_file = './app/data/' + secure_filename(file.filename)
            session_file = './app/data/sessions.csv'

            ex_type_based = ExecutionTypeTest()
            returned_data = ex_type_based.run_execution_type_static(message_file=message_file,
                                                                    session_file=session_file, no_of_lines=0,
                                                                    time_delta=420)

    return render_template('preprocess/preprocess.html', data=json.loads(json.dumps(returned_data)))
    # return redirect(url_for('preprocess_route.show_template', data=json.loads(json.dumps(returned_data)), code=307))
