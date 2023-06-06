from flask_login import UserMixin
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(40), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship to call user.comments and comment.user
    comments = db.relationship('Comment', backref='user')

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

    # Relationship to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
	
    def __repr__(self):
        return "<Title: {}>".format(self.title)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='comments')
    event = db.relationship('Event', backref='comments')

    def __repr__(self):
        return f"<Comment id={self.id} content='{self.content[:20]}...' timestamp={self.timestamp}>"
