from . import app
from models import db, User, Category, Event
from forms import CategoryForm, EventForm, LoginForm
from flask import render_template, request, redirect, url_for, flash
import datetime

# **********
from flask_login import LoginManager

USER = 'admin'
PASSWORD = '1234'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        # Login and validate the user.
        # user should be an instance of your `User` class
        if form.user.data == USER:
            print 'jander'
            flash('Logged in successfully.')

        next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return abort(400)

        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
# **********


# home
@app.route('/')
def home():
    return render_template('home.html')


# 404
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html')


# JSON
@app.route('/JSON')
def json():
    return render_template('home.html')


# new category
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(name=form.name.data)
        db.session.add(newCategory)
        db.session.commit()
        flash("New category created!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('new_category.html', form=form)


# show categories
@app.route('/categories')
def showCategories():
    categories = Category.query.order_by(Category.name)
    return render_template('show_categories.html', categories=categories)


# edit category
@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        cat.name = request.form['name']
        db.session.commit()
        flash("Category updated!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('edit_category.html', cat=cat, form=form)


# delete category
@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    if request.method == 'POST':
        db.session.delete(cat)
        db.session.commit()
        flash("Category deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('delete_category.html', cat=cat)


# new event
@app.route('/event/new', methods=['GET', 'POST'])
def newEvent():
    form = EventForm(request.form)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name)]
    if request.method == 'POST' and form.validate():
        newEvent = Event(
            category_id = form.category_id.data,
            name = form.name.data,
            location = form.location.data,
            date = form.date.data
        )
        db.session.add(newEvent)
        db.session.commit()
        flash('New event created!')
        return redirect(url_for('showEvents'))
    else:
        return render_template('new_event.html', form=form)


# show events
@app.route('/events')
def showEvents():
    eventList = []
    oldEvent = ''
    events = Event.query.order_by(Event.category_id)
    for event in events:
        eventDict = {
            'id': event.id,
            'category_name': event.category.name,
            'name': event.name,
            'location': event.location,
            'date': event.date
        }
        newEvent = event.category.name
        if newEvent == oldEvent:
            eventDict['category_name'] = False
        else:
            oldEvent = newEvent
        eventList.append(eventDict)
    return render_template('show_events.html', events=eventList)


# edit event
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def editEvent(event_id):
    event = Event.query.filter_by(id=event_id).one()
    form = EventForm(request.form)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name)]
    if request.method == 'POST' and form.validate():
        event.category_id = request.form['category_id']
        event.name = request.form['name']
        event.location = request.form['location']
        event.date = datetime.datetime.strptime(request.form['date'], '%d/%m/%Y').date()
        db.session.commit()
        flash("Event updated!")
        return redirect(url_for('showEvents'))
    else:
        return render_template('edit_event.html', event=event, form=form)


# delete event
@app.route('/events/<int:event_id>/delete', methods=['GET', 'POST'])
def deleteEvent(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted!')
        return redirect(url_for('showEvents'))
    else:
        return render_template('delete_event.html', event=event)
