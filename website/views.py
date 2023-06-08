from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .models import Event, Comment
from .forms import EventCreationForm, CommentForm
from . import db
import uuid, os
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

# @bp.route('/user')
# def user():
#     return render_template('user.html')

@bp.route('/event/<id>')
def event(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = CommentForm()
    return render_template('event.html', event=event, form=form)

@bp.route('/event/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==event))

    if form.validate_on_submit():  
        comment = Comment(
            content=form.content.data, 
            event=event, 
            user=current_user
        ) 
        db.session.add(comment) 
        db.session.commit() 
        print('User comment has been added', 'success')

    return redirect(url_for('main.event', id=event.id))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    create_form = EventCreationForm()
    print('User has requested the event creation page...')

    if request.method == 'POST':

        if create_form.validate_on_submit():
            print('User has submitted the event creation form for validation...')
            # Build a filename for the image path
            filename = str(uuid.uuid4())
            uploaded_file = create_form.image.data
            secure_filename(uploaded_file.filename)
            # Set the image path to the static folder
            save_path = os.path.join('website/static/img', filename)
            uploaded_file.save(save_path)
        
            event = Event(
                title=create_form.title.data,
                description=create_form.description.data,
                image=filename,
                dateTime=create_form.dateTime.data,
                price=create_form.price.data,
                ticketsAvailable=create_form.ticketsAvailable.data,
                locationName=create_form.locationName.data,
                status="Open",
                category="Food",
                user=current_user
            )
            
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('main.index'))
     
    return render_template('create.html', create_form=create_form)
    
@bp.route('/bookings')
def bookings():
    return render_template('bookings.html')