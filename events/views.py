from flask import render_template, request, redirect, url_for, flash, session,\
    jsonify
from flask_login import LoginManager, login_user, login_required
import datetime
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from . import app
from models import db, User, Category, Event
from forms import CategoryForm, EventForm, LoginForm


# creation of the database if does not exist
db.create_all()

# import data from the Google JSON file
CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    Connect with Google authentication, from the Udacity course
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'),
            200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    session['user_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = '<h1>Welcome, ' + login_session['username'] + '!</h1>'
    flash("Logged in as %s" % login_session['username'])
    return output


# inititate the Flask login manager
login_manager = LoginManager()
login_manager.init_app(app)


# login manager
@login_manager.user_loader
def load_user(user_id):
    '''
    Check if the user is logged in.
    user_id is the id of the user to be checked.
    Returns the user object if the user is logged in or None if not.
    '''
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
    '''
    Logs an existing user in. Checks if the user already exists.
    Returns a redirect to the home page after login in case of POST or the log
    in html page in case of GET.
    '''
    # Create anti-forgery state token
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32)
        )
    login_session['state'] = state
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
        flash('User does not exist')
        return redirect(url_for('home'))
    return render_template('login.html', form=form, STATE=state)


# log out
@app.route('/logout')
def logout():
    '''
    Logs the user out if is logged in.
    Returns a redirect to the home page.
    '''
    if session['username']:
        session.clear()
        flash('User logged out')
        return redirect(url_for('home'))


# sign In
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    '''
    Creates a new User in the database. Checks if the user already exists and
    logs the user in after adding it to the database.
    Returns a redirect to the home page after login inc ase of POST or the sign
    in html page in case of GET.
    '''
    # Create anti-forgery state token
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32)
        )
    login_session['state'] = state
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
        return render_template('signin.html', form=form, STATE=state)


# 401 unauthorized
@app.errorhandler(401)
def custom_401(error):
    '''
    Renders the unauthorized html page in case of error 401.
    '''
    if 'username' in session:
        session.clear()
        return render_template('session-expired.html')
    return render_template('401.html')


# 404 not found
@app.errorhandler(404)
def pageNotFound(error):
    '''
    Renders the not found html page in case of error 404.
    '''
    return render_template('404.html')


# home
@app.route('/')
def home():
    '''
    Home page.
    Returns a redirect to the show events html page.
    '''
    return redirect(url_for('showEvents'))


# JSON categories
@app.route('/categories/json')
def jsonCategories():
    '''
    JSON format for the categories table.
    Returns the categories in JSON format.
    '''
    categories = Category.query.order_by(Category.name).all()
    return jsonify(Categories=[cat.serialize for cat in categories])


# JSON events
@app.route('/events/json')
def jsonEvents():
    '''
    JSON format for the events table.
    Returns the events in JSON format.
    '''
    events = Event.query.order_by(Event.name).all()
    return jsonify(Events=[ev.serialize for ev in events])


# new category
@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    '''
    Add a category, requires to be logged and makes the user the category
    owner.
    Returns a redirect to show categories after adding the category in case of
    POST or the add category html page in case of GET.
    '''
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(
            name=form.name.data,
            username=session['username']
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
    '''
    Show all categories order by category name, does not require to be logged
    and checks if the user is the category owner in the html rendered file in
    order to allow edition and deletion.
    Returns a render of the show categories html page.
    '''
    categories = Category.query.order_by(Category.name).all()
    for category in categories:
        category.count_events = len(category.events)
    return render_template('show_categories.html', categories=categories)


# show category members
@app.route('/show-category-members/<int:category_id>')
def showCategoryMembers(category_id):
    '''
    Show all the events related to a category ordered by date , does not
    require to be logged and checks if the user is the category owner in the
    html rendered file in order to allow edition and deletion.
    category_id is the id of the category to find events in.
    Returns a render of the show category members html page.
    '''
    events = Event.query.filter_by(category_id=category_id).order_by(
        Event.date
        )
    return render_template('show_category_members.html', events=events)


# edit category
@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    '''
    Edit a category, requires to be logged and checks if the user is the
    category owner in the html rendered file.
    category_id is the id of the category to be edited.
    Returns a redirect to show categories after edition in case of POST or the
    edit category html page in case of GET.
    '''
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
    '''
    Delete a category, requires to be logged and checks if the user is the
    category owner in the html rendered file. Checks if the category is empty
    of events before allowing to delete it.
    category_id is the id of the category to be deleted.
    Returns a redirect to show categories after deletion in case of POST or the
    delete category html page in case of GET.
    '''
    cat = Category.query.filter_by(id=category_id).first()
    if request.method == 'POST':
        category = Category.query.filter_by(id=category_id).first()
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
    '''
    Add an event, requires to be logged and makes the user the event owner.
    Fills the choices select field with all the available categories.
    Returns a redirect to show events after adding the event in case of POST
    or the add event html page in case of GET.
    '''
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
            username=session['username']
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
    '''
    Show all events order by category name and event date, does not require to
    be logged and checks if the user is the event owner in the html rendered
    file in order to allow edition and deletion.
    Returns a render of the show events html page.
    '''
    events = Event.query.join(Category).order_by(
        Category.name, Event.date
        ).all()
    return render_template('show_events.html', events=events)


# edit event
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def editEvent(event_id):
    '''
    Edit an event, requires to be logged and checks if the user is the event
    owner in the html rendered file.
    event_id is the id of the category to be edited.
    Returns a redirect to show events after event edition in case of POST
    or the edit event html page in case of GET
    '''
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
    '''
    Delete an event, requires to be logged and checks if the user is the event
    owner in the html rendered file.
    event_id is the id of the event to be deleted.
    Returns a redirect to show events after deletion in case of POST or the
    delete event html page in case of GET
    '''

    event = Event.query.filter_by(id=event_id).first()
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted')
        return redirect(url_for('showEvents'))
    else:
        return render_template('delete_event.html', event=event)
