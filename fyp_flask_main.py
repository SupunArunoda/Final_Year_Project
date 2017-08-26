from flask import Flask, render_template
from app.preprocess_route import preprocess_route

app = Flask(__name__)
app.register_blueprint(preprocess_route, url_prefix='/preprocess')

if __name__ == '__main__':
    app.run()


@app.route('/')
def show():
    return render_template('index.html')
