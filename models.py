"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
  image_url = db.Column(db.String(150), default=DEFAULT_IMAGE_URL)

  def __repr__(self):
    """Show info about User."""

    u = self
    return f"<User {u.first_name} {u.last_name} {u.image_url}>"

  @classmethod
  def get_by_first_name(cls, name):
    """Get all first_names matching that names."""

    return cls.query.filter_by(first_name=name).all()