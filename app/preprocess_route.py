from flask import Blueprint, render_template

preprocess_route = Blueprint('preprocess_route', __name__, template_folder='templates')


@preprocess_route.route('/')
@preprocess_route.route('/preprocess')
def show():
    return render_template('preprocess/preprocess.html')
