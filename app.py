"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def redirct_to_users():
  return redirect("/users")

@app.route("/users")
def list_users():

  users = User.query.all()
  # print (f"Users info {users}")
  # print (f"Users info {users[0]}")

  return render_template("users.html", users=users)

@app.route("/users/new")
def show_user_form():
  return render_template("create-user.html")


@app.route("/users/new", methods=["POST"])
def create_user():
  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  if request.form["image-url"]:
    image_url = request.form["image-url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  else:
    new_user = User(first_name=first_name, last_name=last_name)

  db.session.add(new_user)
  db.session.commit()

  return redirect("/")

@app.route("/users/<username>")
def show_user_details(username):
  user_details = User.query.get(username)
  print (f"this is the user image {user_details.image_url}")
  return render_template("user-detail.html", user_name=username, image_url = user_details.image_url)

@app.route("/user/<username>/edit")
def edit_user(username):
  return render_template("edit-user.html")

@app.route("/user/<username>/edit", methods=["POST"])
def edit_user_form(username):
  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"]

  updated_user = User.query.get(username)
  print(f"the new user is {updated_user}")
  updated_user.first_name = first_name
  updated_user.last_name = last_name
  updated_user.image_url = image_url

  db.session.commit()

  return redirect("/")

@app.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
  
  delete_user = User.query.get(username)

  db.session.delete(delete_user)

  db.session.commit()

  return redirect("/")