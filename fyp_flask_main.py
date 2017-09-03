from flask import Flask, render_template
from app.PreprocessRoute import preprocess_route
from app.PreprocessMain import preprocess_main

import pymysql


app = Flask(__name__)



app.register_blueprint(preprocess_route, url_prefix='/preprocess')
app.register_blueprint(preprocess_main, url_prefix='/preprocess_main')

if __name__ == '__main__':
    app.run()


@app.route('/')
def show():
    return render_template('index.html')


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
