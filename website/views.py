from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from .models import Event, Comment, Booking
from .forms import EventCreationForm, CommentForm, BookingForm
from . import db
import uuid, os
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    categories = db.session.scalars(db.select(Event.category).distinct())
    return render_template('index.html', events=events, categories=categories)

@bp.route('/<category>')
def category(category):
    exists = Event.query.filter_by(category=category).first()
    if exists is None:
        abort(404)
    events = db.session.scalars(db.select(Event).where(Event.category==category))
    categories = db.session.scalars(db.select(Event.category).distinct())
    return render_template('index.html', events=events, categories=categories)

@bp.route('/event/<id>')
def event(id):
    exists = Event.query.filter_by(id=id).first()
    if exists is None:
        abort(404)
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if datetime.now() > event.dateTime:
        event.status="Inactive"
        db.session.commit() 
        flash('This event is now inactive.')
    comment_form = CommentForm()
    booking_form = BookingForm()
    return render_template('event.html', event=event, comment_form=comment_form, booking_form=booking_form)

@bp.route('/event/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==event))

    if form.validate_on_submit():  
        comment = Comment(
            content=form.content.data, 
            event=event, 
            user=current_user,
            timestamp=datetime.now()
        ) 
        db.session.add(comment) 
        db.session.commit() 
        print('User comment has been added', 'success')
        flash('Your comment has been added.')

    return redirect(url_for('main.event', id=event.id))

@bp.route('/event/<event>/booking', methods=['GET', 'POST'])  
@login_required
def booking(event):  
    form = BookingForm()  
    event = db.session.scalar(db.select(Event).where(Event.id==event))

    if form.validate_on_submit():
        tickets=form.tickets.data
        
        if tickets > event.ticketsAvailable or tickets <= 0 or event.ticketsAvailable == 0:
            print('Booking failed')
            flash('Your order cannot be placed.')
        else:
            event.ticketsAvailable-=tickets
            booking = Booking(
                ticketNum=tickets, 
                event=event, 
                user=current_user
                )
            db.session.add(booking) 
            db.session.commit() 
            print('Booking added', 'success')
            flash('Thank you! Your booking is complete.')

            if event.ticketsAvailable == 0: 
                event.status="Sold out"
                db.session.commit() 
                print('Event sold out!')

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
            # Get the uploaded file
            uploaded_file = create_form.image.data
            # Get the file extension
            _, file_extension = os.path.splitext(uploaded_file.filename)
            # Build a secure filename and append the extension
            secure_filename(uploaded_file.filename)
            filename_with_extension = filename + file_extension
            # Set the image path to the static folder
            save_path = os.path.join('website/static/img/user_events', filename_with_extension)
            # Save the uploaded file to the filesystem with the file path built above
            uploaded_file.save(save_path)
        
            event = Event(
                title=create_form.title.data,
                description=create_form.description.data,
                image='/static/img/user_events/' + filename_with_extension,
                dateTime=create_form.dateTime.data,
                price=create_form.price.data,
                ticketsAvailable=create_form.ticketsAvailable.data,
                locationName=create_form.locationName.data,
                status="Open",
                category=create_form.category.data,
                user=current_user
            )
            
            db.session.add(event)
            db.session.commit()
            flash('Thank you! Your event has been created.')

            return redirect(url_for('main.index'))
     
    return render_template('create.html', create_form=create_form)

@bp.route('/cancel/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel(id):
    event = Event.query.get(id)

    event.status = "Cancelled"
    db.session.commit()
    flash('Your event has been cancelled.')
    
    return redirect(url_for('auth.user'))