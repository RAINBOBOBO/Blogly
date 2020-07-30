"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def root():
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
  image_url = request.form["image-url"] or None
  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()
  flash(f"Adding user {first_name}")
  return redirect("/users")

@app.route("/users/<id>")
def show_user_details(id):
  user_details = User.query.get(id)
  return render_template("user-detail.html", user_details=user_details)

@app.route("/user/<id>/edit")
def edit_user(id):
  user_details = User.query.get(id)
  return render_template("edit-user.html", user_details=user_details)

@app.route("/user/<id>/edit", methods=["POST"])
def edit_user_form(id):
  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"] or None

  updated_user = User.query.get(id)
  print(f"the new user is {updated_user}")
  updated_user.first_name = first_name
  updated_user.last_name = last_name
  updated_user.image_url = image_url

  db.session.commit()
  flash(f"Editing details of {first_name}")
  return redirect("/users")

@app.route("/user/<int:id>/delete", methods=["POST"])
def delete_user(id):
  print (f"inside delete method")
  delete_user = User.query.get(id)

  db.session.delete(delete_user)

  db.session.commit()

  return redirect("/users")