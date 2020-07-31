"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'

connect_db(app)
db.create_all()

@app.route("/")
def root():
  ''' redirects to users page '''

  return redirect("/users")

@app.route("/users")
def list_users():
  ''' Gets all the user details and pass it on to users page to list them  '''

  users = User.query.all()
  return render_template("users.html", users=users)

@app.route("/users/new")
def show_user_form():
  ''' Renders the create user page with a flash message to infrom the user '''

  flash(f"Adding user")
  return render_template("create-user.html")


@app.route("/users/new", methods=["POST"])
def create_user():
  ''' Collects the inputs from the form and creates an instance of User by passing the details collected.
      Adds instance to session and saves the same.
      Redirects to users page '''

  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"] or None

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

  db.session.add(new_user)
  db.session.commit()
  return redirect("/users")

@app.route("/users/<id>")
def show_user_details(id):
  '''Collects the User details and their posts and passes on the info to user details page '''

  user_details = User.query.get(id)
  user_posts = user_details.user_posts
  return render_template("user-detail.html", user_details=user_details, user_posts=user_posts)

@app.route("/user/<id>/edit")
def edit_user(id):
  '''Gets the user details and passes it to edit user page with the flash message '''
  
  user_details = User.query.get(id)
  flash(f"Editing details of {user_details.first_name}")
  return render_template("edit-user.html", user_details=user_details)

@app.route("/user/<id>/edit", methods=["POST"])
def edit_user_form(id):
  '''Collects the updated user details from "Form" and 
  gets the user instance and updates it with new values
  and redirects to users route'''

  first_name = request.form["first-name"]
  last_name = request.form["last-name"]
  image_url = request.form["image-url"] or None

  updated_user = User.query.get(id)
  
  updated_user.first_name = first_name
  updated_user.last_name = last_name
  updated_user.image_url = image_url

  db.session.commit()
  return redirect("/users")

@app.route("/user/<int:id>/delete", methods=["POST"])
def delete_user(id):
  '''gets the user id and deletes it from db 
  and redirects to users route '''
  
  delete_user = User.query.get(id)

  db.session.delete(delete_user)

  db.session.commit()

  return redirect("/users")

@app.route("/users/<int:id>/posts/new")
def show_create_post_form(id):
  '''gets the user details, passes it to create post page and renders create post page'''

  user_details = User.query.get(id)
  return render_template("create-post.html", user_details=user_details)

@app.route("/users/<int:id>/posts/new", methods=["POST"])
def create_post(id):
  '''Collects info from "Form" and creates instance of Post
  and adds it to session and saves to db
  redirects to users/id route '''

  title = request.form["post-title"]
  content = request.form["post-content"]
  new_post = Post(title=title, content=content, user_id=id)

  db.session.add(new_post)
  db.session.commit()
  
  return redirect(f"/users/{id}")

@app.route("/posts/<int:id>")
def show_post(id):
  '''Gets the details of post and passes it to post details page and renders the same '''

  post_details = Post.query.get(id)
  return render_template("post-detail.html", post_details=post_details)

@app.route("/posts/<int:id>/edit")
def show_edit_post(id):
  '''Gets the user and post details and passes it to edit post page and renders the same'''

  post_details = Post.query.get(id)
  user_details = post_details.user_id
  return render_template(f"edit-post.html", user_details=user_details, post_details=post_details)

@app.route("/posts/<int:id>/edit", methods=["POST"])
def edit_post(id):
  '''Collects the updated post details from "Form" and 
  gets the post instance and updates it with new values
  and redirects to posts/id route'''

  new_title = request.form["post-title"]
  new_content = request.form["post-content"] 
  
  post_details = Post.query.get(id)
  post_details.title = new_title
  post_details.content = new_content

  db.session.commit()

  return redirect(f"/posts/{id}")

@app.route("/posts/<int:id>/delete", methods=["POST"])
def delete_post(id):
  '''gets the user id and deletes it from db 
  and redirects to users route '''

  print (f"inside delete method")
  delete_post = Post.query.get(id)

  db.session.delete(delete_post)

  db.session.commit()

  return redirect(f"/users/{id}")