from flask import Blueprint, render_template, request, json

preprocess_route = Blueprint('preprocess_route', __name__, template_folder='templates')


@preprocess_route.route('/')
@preprocess_route.route('/preprocess')
def show_template():
    # print("Total rows: ", request.args.get('data'))
    return render_template('preprocess/preprocess.html')
