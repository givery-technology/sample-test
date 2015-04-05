import json, http.client
from . import db
from flask import Response

DATETIMEFMT = "%Y-%m-%d %H:%M:%S"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    group_id = db.Column(db.Integer)
    events = db.relationship('Event')
    attends = db.relationship('Attend')
    token = db.relationship('Token')

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
    attends = db.relationship('Attend')

    def __init__(self, user, name, start_date):
        self.user = user
        self.name = name
        self.start_date = start_date

    def __repr__(self):
        return '<Event %r>' % self.name


class Attend(db.Model):
    __tablename__ = 'attends'
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event = db.relationship('Event')
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    reserved_at = db.Column(db.DateTime)

    def __init__(self, user, event):
        self.user = user
        self.event = event

    def __repr__(self):
        return '<Attend %r>' % self.event.name


class Token(db.Model):
    __tablename__ = 'tokens'
    token = db.Column(db.String(100), primary_key=True)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, token, user):
        self.token = token
        self.user = user

    def __repr__(self):
        return '<Token %r>' % self.token


class ApiResponse(object):
    def json_response(self):
        self.body.update({'code':self.code})
        return Response(json.dumps(self.body), status=self.http_status, mimetype='application/json')


class LoginResponse(ApiResponse):
    """
    Login response helper
    """
    def __init__(self, token, user, code, http_status=http.client.OK):
        self.body = {'token':token.token, 'user':{'id':user.id, 'name':user.name, 'group_id':user.group_id}}
        self.code = code
        self.http_status = http_status


class UserEventsResponse(ApiResponse):
    """
    User events response helper
    """
    def __init__(self, events, code, http_status=http.client.OK):
        self.body = {'events':[
            {'id':e.id,'name':e.name,'start_date':e.start_date.strftime(DATETIMEFMT),
                'company':{'id':e.user.id,'name':e.user.name}}
            for e in events
            ]}
        self.code = code
        self.http_status = http_status


class CompanyEventsResponse(ApiResponse):
    """
    Company events response helper
    """
    def __init__(self, events, code, http_status=http.client.OK):
        self.body = {'events':[
            {'id':e.id,'name':e.name,'start_date':e.start_date.strftime(DATETIMEFMT),
                'number_of_attendees':len(e.attends)}
            for e in events
            ]}
        self.code = code
        self.http_status = http_status


class StatusResponse(ApiResponse):
    """
    User reserve response helper
    """
    def __init__(self, code, message=None, http_status=http.client.OK):
        self.code = code
        self.body = {}
        if None != message:
            self.body.update({'message':message})
        self.http_status = http_status
