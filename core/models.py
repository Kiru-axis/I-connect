import os
from flask import current_app
from itsdangerous import TimedSerializer
from datetime import datetime
from flask_login import UserMixin
from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# Association table

followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.Text, default="my bio")
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(25), nullable=True, default="avatar.png")
    blog = db.relationship("Blog", backref="user", lazy=True)
    comment = db.relationship("Comment", backref="user", lazy=True)
    likes = db.relationship("Like", backref="user", lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    # followers relationships
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_reset_token(self, expiresAt=1800):
        s = TimedSerializer(
            current_app.config["SECRET_KEY"],
            expiresAt,
        )
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verfy_reset_token(token):

        s = TimedSerializer(
            current_app.config["SECRET_KEY"],
        )

        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f"User({self.username,self.email,self.id,self.followers,self.password,self.followed})"


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime(timezone=True), nullable=False, default=db.func.now()
    )
    image = image = db.Column(db.String(25), nullable=True, default="default.png")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment = db.relationship("Comment", backref="blog", lazy=True)
    likes = db.relationship("Like", backref="blog", lazy=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    # comments callback functions
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        try:
            os.remove(
                path=os.path.join(current_app.root_path, "static/blogs/", self.image)
            )
        except:
            pass

    def get_comment(id):
        comment = Comment.query.all(id=id)
        return comment

    def __repr__(self):
        return f"Blog_id: {self.id}, Author: {self.user.username}, Posted: {self.date_posted}"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.now)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def get_comment(id):
        comment = Comment.query.all(id=id)
        return comment

    def __repr__(self):
        return f"Comment_id: {self.id}, Author: {self.user.username}, Blog_id: {self.blog.id}, Comment:{self.comment}"


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def __repr__(self):
        return f"Like ({self.id,self.blog_id,self.user.username}"
