"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
DEFAULT_IMAGE_URL = "https://paradisevalleychristian.org/wp-content/uploads/2017/01/Blank-Profile.png"



class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(30),
                     nullable=False,
                     unique=True)
    image_url = db.Column(db.Text,
                     nullable=True,
                     default=DEFAULT_IMAGE_URL)
    

class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(30),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    user = db.relationship('User', backref="posts")

class Tag(db.Model):
    """Tag"""
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                      nullable=False,
                      unique = True)
    posts = db.relationship('Post', secondary='posts_tags', cascade="all,delete", backref='tags')
    
    
class PostTag(db.Model):
    """PostTag"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)





 