"""Blogly application."""

from flask import Flask, flash, redirect, render_template, session
from sqlalchemy import text

from models import connect_db, db

app = Flask(__name__)
app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.route("/")
def home():
    return render_template("home.html")


# if __name__ == "__main__":
#     app.run(debug=True)
