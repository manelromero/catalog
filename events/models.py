from . import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8))
    password = db.Column(db.String(10))

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
    events = db.relationship('Event', backref='category', lazy='select')
    user_id = db.Column(db.Integer)

    @property
    def serialize(self):
        # returns category data in in serializeable format
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
            }


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    location = db.Column(db.String(25))
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer)

    @property
    def serialize(self):
        # returns category data in serializeable format
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'date': self.date.strftime("%d/%m/%Y"),
            'category_id': self.category_id,
            'user_id': self.user_id
            }
