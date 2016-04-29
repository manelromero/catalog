from . import app, session
from models import Category, Event
from flask import render_template, request, redirect, url_for

@app.route('/')
def showCategories():
	categories = session.query(Category)
	return render_template('show_categories.html', categories=categories)