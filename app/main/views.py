from flask import render_template,redirect,url_for,abort,request,flash
from . import main
from ..request import get_quotes
from app.models import User,Blog,Comment,Subscriber
from .. import db
from .forms import UpdateProfile,CreateBlog
from flask_login import login_required,current_user


# main/home route 
@main.route('/')
def index():
    quotes = get_quotes()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.order_by(Blog.posted.desc()).paginate(page = page, per_page = 3)
    return render_template('index.html', quote = quotes,blogs=blogs)

# Setting profile picture
@main.route('/profile',methods = ['POST','GET'])
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

# Updating profile
@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/updateprofile.html',form =form)
