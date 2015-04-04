import json, hashlib

from flask import Flask, Response, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cody:cody@localhost/cody'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(160))
    email = db.Column(db.String(120), unique=True)
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
    name = db.Column(db.String(80), unique=True)
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

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8888)