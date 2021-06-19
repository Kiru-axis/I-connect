from flask import render_template,redirect,url_for,abort,request,flash
from . import main
from ..request import get_quotes
from app.models import User,Blog,Comment,Subscriber
from .. import db
@main.route('/')
def index():
  quotes = get_quotes()
  heading = 'Working.. Good to go'
  return render_template('index.html', heading=heading,quote = quotes)