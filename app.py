"""Blogly application."""

from flask import Flask, flash, redirect, render_template, request, url_for

from models import Post, User, connect_db, db, default_img

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def redirect_to_users():
    return redirect(url_for("home_page"))


@app.route("/users", methods=["GET"])
def home_page():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", title="Users Listing", users=users)


@app.route("/users/new", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        img_url = request.form.get("img-url") or default_img

        new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
        db.session.add(new_user)
        db.session.commit()

        flash("User successfully added!", category="success")
        return redirect(url_for("home_page"))
    return render_template("create_user.html", title="Create User")


@app.route("/users/<int:user_id>", methods=["GET"])
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template(
        "user_details.html", title="User details", user=user, posts=posts
    )


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", title="Edit User", user=user)


@app.route("/users/<int:user_id>/submit", methods=["POST"])
def submit_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        img_url = request.form.get("img-url")
        user.first_name = first_name
        user.last_name = last_name
        if not img_url:
            print("no new image entered")
        else:
            user.image_url = img_url

        db.session.commit()
        flash("User info edited!", category="success")
    return redirect(url_for("user_details", user_id=user.id))


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):

    user = User.query.get(user_id)

    if user:
        for post in user.posts:
            db.session.delete(post)

        db.session.delete(user)
        db.session.commit()
        flash(
            f"User {user.get_full_name()} deleted successfully!",
            category="success",
        )
    else:
        flash("User not found or already deleted", category="error")
    return redirect(url_for("home_page"))


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)
    user = post.user
    return render_template("post.html", title="User Post", user=user, post=post)


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def submit_post(user_id):
    user = User.query.get(user_id)

    if request.method == "POST":
        title = request.form.get("post-title")
        content = request.form.get("post-content")

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        posts = Post.query.order_by(Post.created_at).all()
        return redirect(url_for("user_details", user_id=user_id, posts=posts))
    else:
        return render_template("create_post.html", title="New Post", user=user)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):

    post = Post.query.get(post_id)

    if request.method == "POST":
        new_title = request.form.get("post-title")
        new_content = request.form.get("post-content")

        post.title = new_title
        post.content = new_content
        db.session.commit()
        flash("Post info edited!", category="success")
        return redirect(url_for("show_post", post_id=post_id))
    else:
        return render_template("/edit_post.html", title="Edit Post", post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):

    post = Post.query.get(post_id)

    if post:
        user_id = post.user_id

        db.session.delete(post)
        db.session.commit()
        flash(
            f"User {post.title} deleted successfully!",
            category="success",
        )
    else:
        flash("Post not found or already deleted", category="error")
    return redirect(url_for("user_details", user_id=user_id))


if __name__ == "__main__":
    app.run(debug=True)
