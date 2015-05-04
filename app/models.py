__author__ = 'mizumoto'

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

'''
CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  group_id int NOT NULL
);
'''
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    evenets = db.relationship('Events', backref='users', lazy='dynamic')

    def __init__(self, name, email, password, group_id):
        self.name = name
        self.email = email
        self.password = password
        self.group_id = group_id


    def __repr__(self):
        return '<User %r>' % self.name


'''
#CREATE TABLE IF NOT EXISTS events (
    id serial PRIMARY KEY,
    user_id int NOT NULL,
    name varchar(100) NOT NULL,
    start_date datetime NOT NULL
);
'''
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, name, start_date):
        self.user_id = user_id
        self.name = name
        self.start_date = start_date

    def __repr__(self):
        return '<Events %r>' % self.name


'''
#CREATE TABLE IF NOT EXISTS attends (
  user_id int NOT NULL,
  event_id int NOT NULL,
  reserved_at timestamp NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, event_id)
);
'''
class Attends(db.Model):
    __tablename__ = 'attends'
    user_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True)
    reserved_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return '<Attends %r>' % self.user_id

