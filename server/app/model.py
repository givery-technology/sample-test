from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    group_id = db.Column(db.Integer)
    events = db.relationship('Event')

    def __init__(self, name, password, email, group_id):
        self.name = name
        self.password = password
        self.email = email
        self.group_id = group_id

    def __repr__(self):
        return '<User %r>' % self.name

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), unique=True)
    start_date = db.Column(db.DateTime)

    def __init__(self, user, name, start_date):
        self.user = user
        self.name = name
        self.start_date = start_date

    def __repr__(self):
        return '<Event %r>' % self.name