from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from app.controller import sample_test
app.register_blueprint(sample_test)