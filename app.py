"""Blogly application."""

from flask import Flask, flash, redirect, render_template, request, url_for

from models import User, connect_db, db, default_img

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db"
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
    return render_template("user_details.html", title="User details", user=user)


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
        db.session.delete(user)
        db.session.commit()
        flash(
            f"User {user.first_name} {user.last_name} deleted successfully!",
            category="success",
        )
    else:
        flash("User not found or already deleted", category="error")
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    app.run(debug=True)
