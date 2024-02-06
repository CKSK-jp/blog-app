"""Models for Blogly."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img = "/static/icons/no-profile-picture-icon.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User ID={u.id} name={u.first_name} {u.last_name} image={u.image_url}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), default=default_img)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # user = db.relationship("User", backref=db.backref("posts", lazy=True))
