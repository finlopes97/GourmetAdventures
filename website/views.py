from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/user')
def user():
    return render_template('user.html')

@bp.route('/event')
def event():
    return render_template('event.html')

@bp.route('/create')
def create():
    return render_template('create.html')

@bp.route('/bookings')
def bookings():
    return render_template('bookings.html')