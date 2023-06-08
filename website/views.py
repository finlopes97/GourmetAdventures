from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .models import Event, Comment, Booking
from .forms import EventCreationForm, CommentForm, BookingForm
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
            user=current_user
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
            flash('Thank you! Your event has been created.')

            return redirect(url_for('main.index'))
     
    return render_template('create.html', create_form=create_form)
    
@bp.route('/bookings')
def bookings():
    return render_template('bookings.html')