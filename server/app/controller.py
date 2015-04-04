import json, hashlib, hmac

from email.utils import parseaddr
from flask import Blueprint, Response, request, abort
from datetime import datetime
from .model import *
from . import app

DATETIMEFMT = "%Y-%m-%d %H:%M:%S"
DATEFMT = "%Y-%m-%d"

sample_test = Blueprint('sample_test', __name__)
tokens = {}

def json_response(code, body={}, http=http.client.OK):
    body.update({'code':code})
    return Response(json.dumps(body), status=http, mimetype='application/json')


@sample_test.route("/api/auth/login", methods=['POST'])
def login():
    for required in ['email', 'password']:
        if required not in request.form:
            return json_response(500)
    email = request.form['email']
    error, check = parseaddr(email)
    if '' == error and '' == check:
        return json_response(400)
    user = User.query.filter_by(email=email).first()
    if user != None:
        password_hash = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
        if hmac.compare_digest(password_hash, user.password):
            token = hashlib.sha1("{}{}{}".format(user.id, password_hash, datetime.utcnow()).encode('utf-8')).hexdigest()
            tokens[token] = user.id
            return json_response(200, {'token':token, 'user':{
                'id':user.id, 'name':user.name, 'group_id':user.group_id
                }})
    return json_response(500)


@sample_test.route("/api/users/events", methods=['GET'])
def user_events():
    events = Event.query
    try:
        from_date = datetime.strptime(request.args['from'], DATEFMT)
        events = events.filter(from_date <= Event.start_date).order_by(Event.start_date)
    except:
        return json_response(400, http=400)

    if 'limit' in request.args:
        try:
            limit = int(request.args['limit'])
            if limit < 1: raise ValueError
            events = events.limit(limit)
        except:
            return json_response(400, http=400)

    if 'offset' in request.args:
        try:
            offset = int(request.args['offset'])
            if offset < 0: raise ValueError
            events = events.offset(offset)
        except:
            return json_response(400, http=400)

    return json_response(200, {
        'events':[
            {'id':e.id,'name':e.name,'start_date':e.start_date.strftime(DATETIMEFMT),
            'company':{'id':e.user.id,'name':e.user.name}}
            for e in events
            ]
        })


@sample_test.route("/api/users/reserve", methods=['POST'])
def reserve():
    event_id = -1
    if 'event_id' in request.form:
        try:
            event_id = int(request.form['event_id'])
        except:
            return json_response(400, {'message':'Invalid event ID'}, 400)

    reserve = False
    if 'reserve' in request.form:
        if 'true' == request.form['reserve']:
            reserve = True
        elif 'false' != request.form['reserve']:
            return json_response(400, {'message':'Invalid reserve value'}, 400)

    token = ''
    if 'token' not in request.form or request.form['token'] not in tokens:
        return json_response(401, {'message':'Invalid auth token. Please login.'})
    else:
        token = request.form['token']

    user = User.query.filter(tokens[token] == User.id).first()
    if 2 == user.group_id:
        return json_response(401, {'message':"Please register to events as an user."})

    event = Event.query.filter(event_id == Event.id).first()
    if event == None:
        return json_response(400, {'message':'Invalid event.'})

    attending = Attend.query.filter(user == Attend.user).filter(event == Attend.event).first()
    if reserve:
        if attending != None:
            return json_response(501, {'message':'Already registered to the event.'})

        db.session.add(Attend(user, event))
        db.session.commit()
        return json_response(200)
    else:
        if attending == None:
            return json_response(502, {'message':'Not registered to the event.'})

        db.session.delete(attending)
        db.session.commit()
        return json_response(200)


@sample_test.route("/api/companies/events", methods=['POST'])
def company_event():
    token = ''
    if 'token' not in request.form or request.form['token'] not in tokens:
        return json_response(401, {'message':'Invalid auth token. Please login.'})
    else:
        token = request.form['token']

    user = User.query.filter(tokens[token] == User.id).first()
    if 1 == user.group_id:
        return json_response(401, {'message':"Please login as a company."})

    events = Event.query
    try:
        from_date = datetime.strptime(request.form['from'], DATEFMT)
        events = events.filter(user == Event.user).filter(from_date <= Event.start_date).order_by(Event.start_date)
    except Exception as e:
        return json_response(400, http=400)

    if 'limit' in request.form:
        try:
            limit = int(request.form['limit'])
            if limit < 1: raise ValueError
            events = events.limit(limit)
        except:
            return json_response(400, http=400)

    if 'offset' in request.form:
        try:
            offset = int(request.form['offset'])
            if offset < 0: raise ValueError
            events = events.offset(offset)
        except:
            return json_response(400, http=400)

    return json_response(200, {
        'events':[
            {'id':e.id,'name':e.name,'start_date':e.start_date.strftime(DATETIMEFMT),
            'number_of_attendees':len(e.attends)}
            for e in events
            ]
        })


@sample_test.route("/tokens/rm", methods=['GET'])
def cleanup():
    global tokens
    t = {}
    t.update(tokens)
    tokens = {}
    return json_response(200, t)
