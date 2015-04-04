import json, hashlib

from flask import Blueprint, Response, request, abort
from datetime import datetime
from .model import *
from . import app

sample_test = Blueprint('sample_test', __name__)
tokens = {}

def json_response(body, status=200):
    return Response(json.dumps(body), status=status, mimetype='application/json')

@sample_test.route("/api/auth/login", methods=['POST'])
def login():
    for required in ['email', 'password']:
        if required not in request.form:
            return json_response({'code':500})
    user = User.query.filter_by(email=request.form['email']).first()
    if type(user) == User:
        password_hash = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
        if password_hash == user.password:
            token = hashlib.sha1("{}{}{}".format(user.id, password_hash, datetime.utcnow()).encode('utf-8')).hexdigest()
            tokens[token] = user.id
            return json_response({'code':200, 'token':token, 'user':{
                'id':user.id, 'name':user.name, 'group_id':user.group_id
                }})
    return json_response({'code':500})

@sample_test.route("/api/users/events", methods=['GET'])
def user_events():
    events = Event.query
    try:
        from_date = datetime.strptime(request.args['from'], "%Y-%m-%d")
        events = events.filter(from_date <= Event.start_date).order_by(Event.start_date)
    except:
        return json_response({'code':400}, 400)

    if 'limit' in request.args:
        try:
            limit = int(request.args['limit'])
            if limit < 1: raise ValueError
            events = events.limit(limit)
        except:
            return json_response({'code':400}, 400)

    if 'offset' in request.args:
        try:
            offset = int(request.args['offset'])
            if offset < 0: raise ValueError
            events = events.offset(offset)
        except:
            return json_response({'code':400}, 400)

    return json_response({
        'code':200,
        'events':[
            {'id':e.id,'name':e.name,'start_date':e.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            'company':{'id':e.user.id,'name':e.user.name}}
            for e in events
            ]
        })

@sample_test.route("/api/users/reserve", methods=['POST'])
def reserve():
    if 'token' not in request.form or request.form['token'] not in tokens:
        return json_response({'code':401, 'message':'Invalid auth token. Please login.'})
    for required in ['event_id', 'reserve']:
        if required not in request.form:
            return json_response({'code':400, 'message':'Invalid auth token. Please login.'},400)
    user = User.query.filter(tokens[request.form['token']] == User.id).first()
    if 2 == user.group_id:
        return json_response({'code':401, 'message':"Forbidden. Please register to events as an user."})

    return json_response({'code':500, 'message':'Internal Server Error'},500)

@sample_test.route("/api/companies/events", methods=['POST'])
def company_event():
    if 'token' not in request.form:
        return json_response({'code':401})

@sample_test.route("/tokens/rm", methods=['GET'])
def cleanup():
    global tokens
    print(tokens)
    tokens = {}
    return ":)"
