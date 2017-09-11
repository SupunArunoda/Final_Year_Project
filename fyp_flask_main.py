from flask import Flask, render_template, request, make_response
from pandas.tseries.offsets import CacheableOffset

from app.PreprocessRoute import preprocess_route
from app.PreprocessMain import preprocess_main
from flask_cors import CORS

import pymysql

app = Flask(__name__)
CORS(app)

app.register_blueprint(preprocess_route, url_prefix='/preprocess')
app.register_blueprint(preprocess_main, url_prefix='/preprocess_main')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def show():
    return render_template('index.html')


@app.route('/testRoute', methods=['GET', 'POST'])
def testFunc():
    if (request.method == 'POST'):
        print('post method')

        print(request.data)

    return 'this is the result'



@app.before_request
def before():
    pass


@app.after_request
def after(req):
    req.direct_passthrough = False
    # print(req.status)
    # print(req.headers)
    # print(req.get_data())
    return req
