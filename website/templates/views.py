from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)
preference_bp = Blueprint('preference', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@preference_bp.route('/select')
def preference():
    return render_template('preferences.html')
