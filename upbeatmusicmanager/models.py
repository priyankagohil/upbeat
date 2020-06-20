from upbeatmusicmanager import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import flask_whooshalchemyplus as wa
from whoosh.analysis import StemmingAnalyzer
from app import app
from flask_whooshalchemyplus import index_all

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    songs = db.relationship('Music',backref='user',lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class Music(db.Model):
    __searchable__ = ['title', 'album', 'singer']
    __analyzer__ = StemmingAnalyzer()
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    song = db.Column(db.String(64),nullable=False)
    title = db.Column(db.String(140),nullable=False)
    album = db.Column(db.String(140))
    singer = db.Column(db.String(140),nullable=False)

    def __init__(self,title,album,singer,song,user_id):
        self.title = title
        self.album = album
        self.singer = singer
        self.user_id = user_id
        self.song = song

    def __repr__(self):
        return f"Song ID: {self.id} --- {self.title} -- singer: {self.singer}"


#wa.init_app(app)
index_all(app)
