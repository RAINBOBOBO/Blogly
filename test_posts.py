from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/blogly-test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostViewsTestCase(TestCase):

  def setUp(self):
    """Add sample post."""
    Post.query.delete()
    User.query.delete()
    db.session.commit()

    user = User(first_name='Shweta', last_name='Hosamani')
    db.session.add(user)
    db.session.commit()

    post = Post(title='Test title', content='This is complicated', user_id=user.id)
    db.session.add(post)
    db.session.commit()

    self.post_id = post.id
    self.user_id = user.id

  def tearDown(self):
    """Clean up any fouled transaction."""

    db.session.rollback()

  def test_create_post(self):
    with app.test_client() as client:
      
      
      d = {"post-title": "new title by shweta", "post-content": "new content"}
      resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)
      print (f"HTML HERE {html}")

      self.assertEqual(resp.status_code, 200)
      self.assertIn('new title by shweta', html)