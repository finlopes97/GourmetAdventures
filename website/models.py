from flask_login import UserMixin
from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
