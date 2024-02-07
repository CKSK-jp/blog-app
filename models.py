"""Models for Blogly."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img = "/static/icons/no-profile-picture-icon.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), default=default_img)

    def __repr__(self):
        return f"<User ID={self.id} name={self.first_name} {self.last_name} image={self.image_url}>"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return f"<Post ID={self.id} Title={self.title} Content={self.content}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag Name={self.name}>"


class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    post = db.relationship(
        "Post", backref=db.backref("post_tags", cascade="all, delete-orphan")
    )
    tag = db.relationship(
        "Tag", backref=db.backref("post_tags", cascade="all, delete-orphan")
    )

    __table_args__ = (db.UniqueConstraint("post_id", "tag_id"),)

    def __repr__(self):
        return f"<PostTag post_id={self.post_id}, tag_id={self.tag_id}>"
