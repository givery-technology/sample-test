__author__ = 'motomizuki'

from flask import Flask
from app.api.auth import module as auth
from app.models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adf|SW+k64vKielnfEg23/+'

# database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://vagrant:vagrant@localhost:3306/vagrant'
db.init_app(app)

# blueprint modules
app.register_blueprint(auth, url_prefix='/api/auth')