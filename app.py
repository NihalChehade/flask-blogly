"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'uuggtthhkk'




app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

tags_list=['Fun', 'Even More', 'Bloop', 'Zope']

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
    image_url=image_url or None
    
    user = User(first_name=first_name, last_name = last_name, image_url= image_url)
    
    db.session.add(user)
    db.session.commit()
    flash(f"{user.first_name} {user.last_name} was added.")
    return redirect("/users") 

@app.route("/users/<int:usr_id>")
def show_user_details(usr_id):
     user = User.query.get_or_404(usr_id)
     return render_template("user_details.html", user=user)


@app.route("/users/<int:usr_id>/edit")
def show_edit_user_form(usr_id):
    user = User.query.get_or_404(usr_id)
    return render_template("edit_user_form.html",user=user)

@app.route("/users/<int:usr_id>/edit", methods=["POST"])
def edit_a_user(usr_id):
    user = User.query.get_or_404(usr_id)
    user.first_name= request.form.get('firstName')
    user.last_name = request.form.get('lastName')
    user.image_url = request.form.get('imgUrl')

    db.session.add(user)
    db.session.commit()
    flash(f"{user.first_name} {user.last_name} was edited.")
    return redirect("/users") 


@app.route("/users/<int:usr_id>/delete", methods=["POST"])
def delete_user(usr_id):
    user = User.query.get_or_404(usr_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.first_name} {user.last_name} was deleted.")
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("add_post_form.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_post(user_id):
  
    title = request.form.get("post-title")
    content = request.form.get("post-content")
    tag_ids = [int(num) for num in request.form.getlist("selected-tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=title, content=content, created_at=None, user_id=user_id, tags=tags)
            
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' was added.")

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post_form.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title= request.form.get('post-title')
    post.content = request.form.get('post-content')

    tag_ids = [int(num) for num in request.form.getlist("selected-tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' updated.")

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")
    return redirect(f"/users/{post.user_id}")



@app.route("/tags")
def list_tags():
    tags = Tag.query.all()
    return render_template("tags_list.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)

@app.route("/tags/new")
def show_add_tag_form():
    posts = Post.query.all()
    return render_template("create_tag_form.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def create_a_tag():
    name=request.form.get("name")
    post_ids = [int(num) for num in request.form.getlist("selected-posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag =Tag(name=name, posts=posts)
    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' was added.")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("edit_tag_form.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_a_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name=request.form.get("name")
    post_ids = [int(num) for num in request.form.getlist("selected-posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' was edited.")
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")
    return redirect("/tags")
