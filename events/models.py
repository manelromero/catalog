from . import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8))
    password = db.Column(db.String(8))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    events = db.relationship(
        'Event',
        backref = 'category',
        lazy = 'select'
    )


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    location = db.Column(db.String(20))
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
