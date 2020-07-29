"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
  base_url = 'https://cdn.dribbble.com/users/2095589/screenshots/4166422/user_1.png'
  __tablename__ = 'users'

  id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
  first_name = db.Column(db.String(20), nullable=False, unique=True)
  last_name = db.Column(db.String(20), nullable=False)
  image_url = db.Column(db.String(50), default=base_url)

