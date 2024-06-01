from flask import (
    redirect,
    request,
    flash,
    render_template,
    abort,
    url_for,
    Blueprint,
    jsonify,
)
from flask_login import current_user, login_required
from core import db
from core.blog.utils import save_blog_image
from core.models import Blog, Comment, Like
from core.blog.forms import CreateBlogForm


blog = Blueprint("blog", __name__)


@blog.route("/blog/<id>")
def blogs(id):
    comments = Comment.query.filter_by(blog_id=id).all()

    blog = Blog.query.get(id)
    return render_template("blog.html", blog=blog, comments=comments)


@blog.route("/new_post", methods=["POST", "GET"])
@login_required
def create_blog():
    """
    Since we are dealing with images,dont forget to add  `enctype="multipart/form-data` on the form
    """
    form = CreateBlogForm()

    if form.validate_on_submit():

        content = form.content.data
        image_file = None
        if form.image.data:
            image_file = save_blog_image(form.image.data)

        blog = Blog(content=content, user_id=current_user.id, image=image_file)
        blog.save()
        flash("Blog created")
        return redirect(url_for("main.index"))
    return render_template(
        "blog/create-blog.html", form=form, form_header="Create Blog"
    )


# Updating blogs section
@blog.route("/blog/<blog_id>/update", methods=["GET", "POST"])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreateBlogForm()
    if form.validate_on_submit():
        blog.content = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for("main.index", id=blog.id))
    if request.method == "GET":
        form.image.data = blog.image
        form.content.data = blog.content
    return render_template(
        "blog/create-blog.html", form=form, form_header="Update Blog"
    )


# Deleting blogs section
@blog.route("/blog/<string:blog_id>/delete", methods=["POST"])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("Blog delete succes!")
    return redirect(url_for("main.index"))


@blog.route("/comment/<blog_id>", methods=["POST", "GET"])
@login_required
def comment(blog_id):

    # check if the blog exists
    Blog.query.get_or_404(blog_id)

    comments = Comment.query.filter_by(blog_id=blog_id, user_id=current_user.id).first()

    if comments:
        flash("You already made a comment for these blog", "info")
        return jsonify({"success": False, "message": "You already made a comment"})

    if request.method == "POST":
        comment_text = request.form.get("comment")
        new_comment = Comment(
            blog_id=blog_id, user_id=current_user.id, comment=comment_text
        )
        new_comment.save()

        # the structure of all comments
        # send it to js

        obj = {
            "user": {
                "image": new_comment.user.image,
                "username": new_comment.user.username,
            },
            "comment": new_comment.comment,
        }
        return jsonify({"comment": obj})


@blog.route("/like/<blog_id>", methods=["POST", "GET"])
@login_required
def like(blog_id):

    # check if the blog exists
    blog = Blog.query.get_or_404(blog_id)

    # check if the user already liked the blog
    liked = Like.query.filter_by(user_id=current_user.id, blog_id=blog_id).first()

    if not blog:
        flash("blog not found", "error")
    elif liked:
        db.session.delete(liked)
        db.session.commit()
    else:
        new_like = Like(
            user_id=current_user.id,
            blog_id=blog.id,
        )
        new_like.save()
    return redirect(url_for("main.index"))
