"""Blogly application."""

from flask import Flask, flash, redirect, render_template, request, session, url_for

from models import User, connect_db, db, default_img

# from sqlalchemy import text


app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home_page():
    users = User.query.all()
    return render_template("users.html", title="Users Listing", users=users)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        img_url = request.form.get("img-url") or default_img

        new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
        db.session.add(new_user)
        db.session.commit()

        flash("User successfully added!", category="success")
        return redirect("/")
    return render_template("create_user.html", title="Create User")


@app.route("/user_details/<int:user_id>", methods=["GET"])
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", title="User details", user=user)


@app.route("/edit_user/<int:user_id>", methods=["GET"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", title="Edit User", user=user)


@app.route("/submit_edit", methods=["POST"])
def submit_edit():
    return render_template("user_details.html")


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form.get("user_id")

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
