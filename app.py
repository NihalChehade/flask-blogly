"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension


app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    
    db.create_all()


@app.route("/")
def home_page():
    """redirects to users route"""

    
    return redirect("/users") 

@app.route("/users")
def list_users():
    """List users."""
    users = User.query.all()
    return render_template("users_list.html", users=users)

@app.route("/users/new")
def new_user_form():
    """ New user form."""

    
    return render_template("add_user_form.html") 


@app.route("/users/new", methods=["POST"])
def add_user():
    """ Add a user and redirect to list of users"""
 
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    image_url = request.form.get('imgUrl')
    image_url=image_url if image_url else None
    
    user = User(first_name=first_name, last_name = last_name, image_url= image_url)
    print(user)
    db.session.add(user)
    db.session.commit()

    return redirect("/users") 

@app.route("/users/<int:usr_id>")
def show_user_details(usr_id):
     user = User.query.get_or_404(usr_id)
     return render_template("user_details.html", user=user)


@app.route("/users/<int:usr_id>/edit")
def show_edit_form(usr_id):
    user = User.query.get_or_404(usr_id)
    return render_template("edit_user_form.html",user=user)

@app.route("/users/<int:usr_id>/edit", methods=["POST"])
def edit_user(usr_id):
    user = User.query.get_or_404(usr_id)
    user.first_name= request.form.get('firstName')
    user.last_name = request.form.get('lastName')
    user.image_url = request.form.get('imgUrl')

    db.session.add(user)
    db.session.commit()
    return redirect("/users") 


@app.route("/users/<int:usr_id>/delete")
def delete_user(usr_id):
    User.query.filter_by(id=usr_id).delete()

    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("add_post_form.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_post(user_id):
  
    title = request.form.get("post-title")
    content = request.form.get("post-content")
    post = Post(title=title, content=content, created_at=None, user_id=user_id)
    

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("edit_post_form.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title= request.form.get('post-title')
    post.content = request.form.get('post-content')
  

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()

    db.session.commit()
    return redirect(f"/users/{post.user_id}")