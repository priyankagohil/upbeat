#upbeatmusicmanager/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_whooshalchemyplus

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

#############################
### DATABASE SETUP ##########
#############################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)
Migrate(app,db)

###############################################################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

###############################################################

from upbeatmusicmanager.core.views import core
from upbeatmusicmanager.users.views import users
from upbeatmusicmanager.songs.views import songs
from upbeatmusicmanager.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(songs)
app.register_blueprint(error_pages)
