from flask_login import UserMixin
from . import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400))
    date = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2))

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
