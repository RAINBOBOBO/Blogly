from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):

  def setUp(self):
    """Add sample user."""

    User.query.delete()

    user = User(first_name='TestUser', last_name='Babauta')
    db.session.add(user)
    db.session.commit()

    self.id = user.id
    
  def tearDown(self):
    """Clean up any fouled transaction."""

    db.session.rollback()

  def test_list_user(self):
    with app.test_client() as client:
      resp = client.get("/users")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('TestUser', html)

  def test_show_user(self):
    with app.test_client() as client:
      resp = client.get(f"/users/{self.id}")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<h1>TestUser</h1>', html)

  def test_add_user(self):
    with app.test_client() as client:
      d = {2,"first-name": "TestUser2", "last-name": "genericlastname", "image-url": 'https://cdn.dribbble.com/users/2095589/screenshots/4166422/user_1.png'}
      resp = client.post("/users/new", data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<li><a href="/users/2">TestUser2</a></li>', html)
