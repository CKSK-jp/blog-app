"""Blogly application."""

from flask import Flask, flash, redirect, render_template, request, url_for

from models import Post, PostTag, Tag, User, connect_db, db, default_img

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    users = User.query.order_by(User.last_name, User.first_name).all()
    posts = Post.query.order_by(Post.created_at.desc()).all()

    post_tags = {}

    for post in posts:
        associated_tags = PostTag.query.filter_by(post_id=post.id).all()
        post_tags[post.id] = [tag_item.tag for tag_item in associated_tags]
    return render_template(
        "home.html", title="Home Page", users=users, posts=posts, post_tags=post_tags
    )


@app.route("/users", methods=["GET"])
def users_page():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", title="Users Listing", users=users)


@app.route("/users/new", methods=["GET"])
@app.route("/users/<int:user_id>/edit", methods=["GET"])
def handle_user(user_id=None):

    # Creating a new user
    if user_id is None:
        action = "Add"
        route = "new"
        btn_class = "add-button"
        btn_name = "Add"
        user = None

    # Edit existing user
    else:
        action = "Edit"
        route = f"{user_id}/submit"
        btn_class = "save-button"
        btn_name = "Save"
        user = User.query.get(user_id)
    return render_template(
        "user_form.html",
        user=user,
        route=route,
        action=action,
        btn_class=btn_class,
        btn_name=btn_name,
    )


@app.route("/users/new", methods=["POST"])
def create_user():
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    img_url = request.form.get("img-url") or default_img

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    flash("User successfully added!", category="success")
    return redirect(url_for("users_page"))


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    posts = user.posts
    return render_template(
        "user_details.html", title="User details", user=user, posts=posts
    )


@app.route("/users/<int:user_id>/submit", methods=["POST"])
def submit_edit(user_id):
    user = User.query.get(user_id)
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
    return redirect(url_for("get_user", user_id=user.id))


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
    return redirect(url_for("users_page"))


# Post routes
@app.route("/posts/<int:post_id>")
def get_post(post_id):
    post = Post.query.get(post_id)
    associated_tags = PostTag.query.filter_by(post_id=post_id).all()
    tags = [tag_item.tag for tag_item in associated_tags]

    user = post.user
    return render_template(
        "post.html", title="User Post", user=user, post=post, tags=tags
    )


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def create_edit_post(user_id=None, post_id=None):
    print("Inside new route")
    user = User.query.get(user_id)
    tags = Tag.query.all()

    # Create a new post
    if post_id is None:
        title = "Create Post"
        action = "Create"
        btn_class = "add-button"
        btn_name = "Add"
        route = f"/users/{user_id}/posts/new"
        post = None
    # Edit existing post
    else:
        title = "Edit Post"
        post = Post.query.get(post_id)
        action = "Edit"
        btn_class = "save-button"
        btn_name = "Save"
        route = f"/posts/{post_id}/edit"

    return render_template(
        "post_form.html",
        title=title,
        user=user,
        post=post,
        tags=tags,
        action=action,
        btn_class=btn_class,
        btn_name=btn_name,
        route=route,
    )


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_post_form(user_id=None, post_id=None):
    title = request.form.get("post-title")
    content = request.form.get("post-content")
    selected_tags = request.form.getlist("tags[]")
    print(f"Selected Tags: {selected_tags}")

    if post_id is None:
        create_post(user_id, title, content, selected_tags)
    else:
        post = Post.query.get(post_id)
        edit_post(post, title, content, selected_tags)
        user_id = post.user_id

    posts = Post.query.order_by(Post.created_at).all()
    flash("Post info updated!", category="success")
    return redirect(url_for("get_post", post_id=post.id, user_id=user_id, posts=posts))


def create_post(user_id, title, content, tags):
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag_id in tags:
        post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
        db.session.add(post_tag)
    db.session.add(new_post)
    db.session.commit()


def edit_post(post, title, content, tags):
    # Update post title and content
    post.title = title
    post.content = content

    post.tags.clear()

    # Add the new tags to the post
    for tag_id in tags:
        tag = Tag.query.get(tag_id)
        if tag:
            post.tags.append(tag)

    # Commit changes to the database
    db.session.commit()


# @app.route("/posts/<int:post_id>/edit", methods=["POST"])
# def edit_post(post_id):

#     post = Post.query.get(post_id)

#     if request.method == "POST":
#         new_title = request.form.get("post-title")
#         new_content = request.form.get("post-content")

#         post.title = new_title
#         post.content = new_content
#         db.session.commit()

#         flash("Post info edited!", category="success")
#     return redirect(url_for("get_post", post_id=post_id))


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
    return redirect(url_for("get_user", user_id=user_id))


# Tag Routes
@app.route("/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    if not tags:
        return render_template("tags.html", title="Tags", tags=[])
    else:
        return render_template("tags.html", title="Tags", tags=tags)


@app.route("/tags/new", methods=["GET"])
@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def handle_tag(tag_id=None):
    if tag_id is None:
        action = "Create"
        route = "new"
        btn_class = "add-button"
        btn_name = "Add"
        return render_template(
            "tag_form.html",
            route=route,
            action=action,
            btn_class=btn_class,
            btn_name=btn_name,
        )
    else:
        action = "Edit"
        route = f"{tag_id}/edit"
        btn_class = "save-button"
        btn_name = "Save"
        return render_template(
            "tag_form.html",
            route=route,
            action=action,
            btn_class=btn_class,
            btn_name=btn_name,
        )


@app.route("/tags/new", methods=["POST"])
@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def create_tag(tag_id=None):
    tags = Tag.query.all()
    tag_names = [tag.name for tag in tags]
    tag_name = request.form.get("tag-name")

    # New tag creation
    if tag_id is None and tag_name not in tag_names:
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()

        tags = Tag.query.all()
        flash("Tag name succesfully added!", category="success")

    # Edit existing tag
    elif tag_id and tag_name not in tag_names:
        edited_tag = Tag.query.get(tag_id)
        edited_tag.name = tag_name
        db.session.commit()
        flash("Tag name succesfully edited!", category="success")
    else:
        flash("Tag name already exists!", category="error")
        return render_template(
            "tag_form.html",
            action="Edit",
            route=f"{tag_id}/edit",
            btn_class="save-button",
            btn_name="Save",
        )
    return redirect(url_for("get_tags", title="Create a Tag", tags=tags))


@app.route("/tags/<int:tag_id>", methods=["GET"])
def get_tag(tag_id):
    tag = Tag.query.get(tag_id)
    post_tag_records = PostTag.query.filter_by(tag_id=tag_id).all()

    post_ids = [record.post_id for record in post_tag_records]

    related_posts = Post.query.filter(Post.id.in_(post_ids)).all()

    return render_template(
        "tag_details.html", title=tag.name, tag=tag, posts=related_posts
    )


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        post_tags = PostTag.query.filter_by(tag_id=tag_id).all()

        for post_tag in post_tags:
            db.session.delete(post_tag)

        db.session.delete(tag)
        db.session.commit()

        flash(
            f"Tag: #{tag.name} deleted successfully!",
            category="success",
        )
    return redirect(url_for("get_tags"))


if __name__ == "__main__":
    app.run(debug=True)
