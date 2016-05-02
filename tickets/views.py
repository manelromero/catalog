from . import app, session
from models import Category, Event
from forms import CategoryForm
from flask import render_template, request, redirect, url_for, flash


# home
@app.route('/')
def home():
    return render_template('home.html')


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
    categories = session.query(Category)
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


# new ticket
@app.route('/ticket/<int:category_id>new')
def newTicket(category_id):
    return render_template('new_ticket.html')


# show tickets
@app.route('/tickets')
def showTickets():
    return render_template('show_tickets.html', categories=categories)


# edit ticket
@app.route('/tickets/<int:category_id>/edit')
def editTicket(category_id):
    return render_template('edit_ticket.html')


# delete ticket
@app.route('/tickets/<int:ticket_id>/delete')
def deleteTicket():
    return render_template('delete_ticket.html')
