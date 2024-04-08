"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


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
                     default="https://paradisevalleychristian.org/wp-content/uploads/2017/01/Blank-Profile.png")
    

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