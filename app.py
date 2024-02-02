"""Blogly application."""

from flask import Flask, flash, redirect, render_template, session

from models import User, connect_db, db

# from sqlalchemy import text


app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///users_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    return render_template("users.html", title="User Home")


@app.route("/create_user.html")
def create_user():
    return render_template("create_user.html", title="Create User")


@app.route("/user_details.html")
def user_details():
    return render_template("user_details.html", title="Create User")


if __name__ == "__main__":
    app.run(debug=True)
