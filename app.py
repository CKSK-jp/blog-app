"""Blogly application."""

from flask import Flask, flash, redirect, render_template, session

from models import Pet, connect_db, db

# from sqlalchemy import text


app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet_shop_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


# if __name__ == "__main__":
#     app.run(debug=True)
