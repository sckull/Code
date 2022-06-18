# App
from app import db

# Flask Login
from flask_login import UserMixin

# Utils
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

user_roles = db.Table('user_roles',
    db.Column('user_id',  db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model, UserMixin):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name  = db.Column(db.String(20), nullable=False)
    about      = db.Column(db.String(60), nullable=True)
    job        = db.Column(db.String(20), nullable=True)
    image      = db.Column(db.String(),   nullable=True, default="static/images/default.png")    
    twitter    = db.Column(db.String(20), nullable=True)
    facebook   = db.Column(db.String(20), nullable=True)
    instagram  = db.Column(db.String(20), nullable=True)
    linkedin   = db.Column(db.String(20), nullable=True)
    github     = db.Column(db.String(20), nullable=True)
    email      = db.Column(db.String(20), nullable=False, unique=True)
    username   = db.Column(db.String(20), nullable=False, unique=True)
    password   = db.Column(db.String(80), nullable=False)
    roles 	   = db.relationship('Role', secondary = user_roles, lazy = 'subquery', backref = db.backref('user_roles', lazy = True))

    def set_password(self, password):        
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        # pw_hash, password (text)
        return bcrypt.check_password_hash(self.password, password)

    def get_username(self):
        return self.username

class Role(db.Model):
    id 	 = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

tags = db.Table('tags',
    db.Column('tag_id',  db.Integer, db.ForeignKey('tag.id',ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id',ondelete='CASCADE'), primary_key=True)
)

class Post(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(100))   
    body            = db.Column(db.String(1800))
    description     = db.Column(db.String(60))
    featured_image  = db.Column(db.String(60), default = "static/images/default/blog.png")
    timestamp       = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    last_edit       = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    published       = db.Column(db.Boolean)
    # huh
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))    
    user_info       = db.relationship('User', backref = db.backref('user', uselist = False))
    tags            = db.relationship('Tag', secondary = tags, lazy = 'subquery', backref = db.backref('posts', lazy = True, passive_deletes=True) )
    

class Tag(db.Model):
    id   = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), unique = True)
    description = db.Column(db.String(80))

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

