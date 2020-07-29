"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def list_users():

  users = User.query.all()

  return render_template("users.html", users=users)

@app.route("/create-user")
def show_user_form():
  return render_template("create-user.html")


@app.route("/create-user", methods=["POST"])
def create_user():
  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"]

  new_user = User(first_name, last_name, image_url)
  db.session.add(new_user)
  db.session.commit()

  return redirect("/")

