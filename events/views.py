from . import app
from models import *
from forms import CategoryForm, EventForm, LoginForm
from flask import render_template, request, redirect, url_for, flash, session,\
    jsonify
import datetime
from flask_login import LoginManager, login_user, login_required


db.create_all()

# inititate the login manager
login_manager = LoginManager()
login_manager.init_app(app)


# login manager
@login_manager.user_loader
def load_user(user_id):
    if 'username' in session:
        user = User(
            id=user_id,
            username=session['username']
            )
        return user
    return None


# log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        loginUser = {
            'username': form.username.data,
            'password': form.password.data
            }
        users = User.query.all()
        # check database is not empty
        if users:
            # check user
            for user in users:
                if user.username == loginUser['username']:
                    if user.password == loginUser['password']:
                        session['username'] = loginUser['username']
                        session['user_id'] = user.id
                        flash('User logged in')
                        return redirect(url_for('home'))
            flash('User does not exist')
            return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        form=form,
        action='login',
        action_name='Log In'
        )


# log out
@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
        flash('User logged out')
        return redirect(url_for('home'))


# sign In
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        newUser = User(
            username=form.username.data,
            password=form.password.data
            )
        users = User.query.all()
        # check database is not empty
        if users:
            # check user doesn't exist
            for user in users:
                if newUser.username == user.username:
                    flash('User already exists, please try another user')
                    return redirect(url_for('signin'))
        db.session.add(newUser)
        db.session.commit()
        users = User.query.all()
        for user in users:
            if user.username == newUser.username:
                session['username'] = user.username
                session['user_id'] = user.id
                flash("User registered")
                return redirect(url_for('home'))
    else:
        return render_template(
            'login.html',
            form=form,
            action='signin',
            action_name='Sign In'
            )


# 401 unauthorized
@app.errorhandler(401)
def custom_401(error):
    if 'username' in session:
        session.clear()
        return render_template('session-expired.html')
    return render_template('401.html')


# 404 not found
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')


# home
@app.route('/')
def home():
    return redirect(url_for('showEvents'))


# JSON categories
@app.route('/categories/json')
def jsonCategories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify(Categories=[cat.serialize for cat in categories])


# JSON events
@app.route('/events/json')
def jsonEvents():
    events = Event.query.order_by(Event.name).all()
    return jsonify(Events=[ev.serialize for ev in events])


# new category
@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(
            name=form.name.data,
            user_id=session['user_id']
            )
        db.session.add(newCategory)
        db.session.commit()
        flash("New category created")
        return redirect(url_for('showCategories'))
    else:
        return render_template('new_category.html', form=form)


# show categories
@app.route('/categories')
def showCategories():
    categories = Category.query.order_by(Category.name).all()
    for category in categories:
        category.count_events = len(category.events)
    return render_template('show_categories.html', categories=categories)


# edit category
@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        cat.name = request.form['name']
        db.session.commit()
        flash("Category updated")
        return redirect(url_for('showCategories'))
    else:
        return render_template('edit_category.html', cat=cat, form=form)


# delete category
@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    if request.method == 'POST':
        category = Category.query.filter_by(id=category_id).first()
        print '\nEVENTS:', category.events
        if category.events == []:
            db.session.delete(cat)
            db.session.commit()            
            flash("Category deleted")
            return redirect(url_for('showCategories'))
        flash("Category has to be empty to delete it")
        return redirect(url_for('showCategories'))
    else:
        return render_template('delete_category.html', cat=cat)


# new event
@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def newEvent():
    form = EventForm(request.form)
    form.category_id.choices = ([
        (c.id, c.name) for c in Category.query.order_by(Category.name)
        ])
    form.category_id.choices.insert(0, (0, 'select'))
    if request.method == 'POST' and form.validate():
        newEvent = Event(
            category_id=form.category_id.data,
            name=form.name.data,
            location=form.location.data,
            date=form.date.data,
            user_id=session['user_id']
        )
        db.session.add(newEvent)
        db.session.commit()
        flash('New event created')
        return redirect(url_for('showEvents'))
    else:
        return render_template('new_event.html', form=form)


# show events
@app.route('/events')
def showEvents():
    eventList = []
    oldEvent = ''
    categories = Category.query.order_by(Category.name).all()
    for category in categories:
        for event in category.events:
            eventDict = {
                'id': event.id,
                'name': event.name,
                'location': event.location,
                'date': event.date,
                'category_name': event.category.name,
                'user_id': event.user_id
            }
            if oldEvent == event.category.name:
                eventDict['category_name'] = False
            else:
                oldEvent = event.category.name
            eventList.append(eventDict)
    return render_template('show_events.html', events=eventList)


# edit event
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def editEvent(event_id):
    event = Event.query.filter_by(id=event_id).one()
    form = EventForm(request.form)
    form.category_id.choices = ([
        (c.id, c.name) for c in Category.query.order_by(Category.name)
        ])
    form.category_id.choices.insert(0, (0, 'select'))
    if request.method == 'POST' and form.validate():
        event.category_id = request.form['category_id']
        event.name = request.form['name']
        event.location = request.form['location']
        event.date = datetime.datetime.strptime(
            request.form['date'], '%d/%m/%Y').date()
        db.session.commit()
        flash("Event updated")
        return redirect(url_for('showEvents'))
    else:
        return render_template('edit_event.html', event=event, form=form)


# delete event
@app.route('/events/<int:event_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteEvent(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted')
        return redirect(url_for('showEvents'))
    else:
        return render_template('delete_event.html', event=event)
