"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'https://cdn.dribbble.com/users/2095589/screenshots/4166422/user_1.png'


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  first_name = db.Column(db.String(20), nullable=False, unique=True)
  last_name = db.Column(db.String(20), nullable=False)
  image_url = db.Column(db.String(250), default=DEFAULT_IMAGE_URL)

  user_posts = db.relationship('models.Post', backref='users')

  def __repr__(self):
    """Show info about User."""

    u = self
    return f"<User {u.first_name} {u.last_name} {u.image_url}>"

  @classmethod
  def get_by_first_name(cls, name):
    """Get all first_names matching that names."""

    return cls.query.filter_by(first_name=name).all()

class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  title = db.Column(db.String(40), nullable=False)
  content = db.Column(db.String(240), nullable=False)
  created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  

  def __repr__(self):
    """Show info about Post."""

    p = self
    return f"<User {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

  @classmethod
  def get_by_id(cls, id):
    """Get all posts matching that id."""

    return cls.query.get(id).all()