from flask_login import UserMixin
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to call user.comments and comment.user
    comments = db.relationship('Comment', backref='user')
    # Relationship call user.bookings, booking.user
    bookings = db.relationship('Booking', backref='user')
    # Relationship call user.events, event.user
    events = db.relationship('Event', backref='user', lazy=True)

    def set_password(self, password):
        # Sets password to a hashed password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Returns True if password is correct
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Username: {}>".format(self.username)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400))
    dateTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2))
    ticketsAvailable = db.Column(db.Integer, nullable=False)
    locationName = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default="Open", nullable=False)
    category = db.Column(db.String(20))
    # Foreign key to users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
    # Relationship call event.bookings, booking.event
    bookings = db.relationship('Booking', backref='event')
	
    def __repr__(self):
        return "<Title: {}>".format(self.title)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"<Comment id={self.id} content='{self.content[:20]}...' timestamp={self.timestamp}>"
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    ticketNum = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Booking ID: {}>".format(self.id)