import json, hashlib

from datetime import datetime

from flask import Flask, Response, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cody:cody@localhost/cody'
db = SQLAlchemy(app)

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

def json_response(body, status=200):
    return Response(json.dumps(body), status=status, mimetype='application/json')

@app.route("/api/auth/login", methods=['POST'])
def login():
    for required in ['email', 'password']:
        if required not in request.form:
            return json_response({'code':500})
    user = User.query.filter_by(email=request.form['email']).first()
    if type(user) == User:
        password_hash = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
        if password_hash == user.password:
            return json_response({'code':200, 'token':'x', 'user':{
                'id':user.id, 'name':user.name, 'group_id':user.group_id
                }})
    return json_response({'code':500})

@app.route("/api/users/events", methods=['GET'])
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

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8888)