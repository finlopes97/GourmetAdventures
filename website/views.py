from flask import Blueprint, render_template
from .models import Event
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

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