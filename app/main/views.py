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

# Updating profile