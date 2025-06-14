from flask import Blueprint
from flask import render_template
from flask import url_for

about = Blueprint('about', __name__, template_folder='templates')
@about.route('/about/')
def show():
    return render_template('about.html')
