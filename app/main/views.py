from flask import render_template,redirect,url_for,abort,request,flash
from . import main

@main.route('/')
def index():
  heading = 'Working.. Good to go'
  return render_template('index.html', heading=heading)