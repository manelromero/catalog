from . import app, session
from models import User, Category, Event
from forms import CategoryForm, EventForm, LoginForm
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

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
    if request.method == 'POST':
        if form.validate():
            newCategory = Category(name=form.name.data)
            session.add(newCategory)
            session.commit()
            flash("New category created!")
            return redirect(url_for('showCategories'))
        else:
            return render_template('new_category.html', form=form)
    else:
        return render_template('new_category.html', form=form, new=True)


# show categories
@app.route('/categories')
def showCategories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('show_categories.html', categories=categories)


# edit category
@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    cat = session.query(Category).filter_by(id = category_id).one()
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        cat.name = request.form['name']
        session.add(cat)
        session.commit()
        flash("Category updated!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('edit_category.html', cat=cat, form=form)


# delete category
@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    cat = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(cat)
        session.commit()
        flash("Category deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('delete_category.html', cat=cat)


# new event
@app.route('/event/new', methods=['GET', 'POST'])
def newEvent():
    form = EventForm(request.form)
    form.category_id.choices = [(c.id, c.name) for c in session.query(Category).order_by(Category.name)]
    if request.method == 'POST':
        print form.category_id.data
        if form.validate():
            newEvent = Event(category_id=form.category_id.data,
                name=form.name.data,
                location=form.location.data,
                date=form.date.data)
            session.add(newEvent)
            session.commit()
            flash('New event created!')
            return redirect(url_for('showEvents'))
        else:
            return render_template('new_event.html', form=form)
    else:
        return render_template('new_event.html', form=form)


# show events
@app.route('/events')
def showEvents():
    events = session.query(Event).order_by(Event.category_id).all()
    return render_template('show_events.html', events=events)


# edit event
@app.route('/events/<int:event_id>/edit')
def editEvent(event_id):
    return render_template('edit_event.html')


# delete event
@app.route('/events/<int:event_id>/delete', methods=['GET', 'POST'])
def deleteEvent(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    if request.method == 'POST':
        session.delete(event)
        session.commit()
        flash('Event deleted!')
        return redirect(url_for('showEvents'))
    else:
        return render_template('delete_event.html', event=event)
