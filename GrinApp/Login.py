"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, session, g
from GrinApp import app
from GrinApp.SQLTool import QueryBuilder
from werkzeug.security import check_password_hash,  generate_password_hash
import functools

# Home page get route
@app.get('/')
def login_get(user="", wrong=False):
    return render_template(
    'login.html',
    title='Login',
    user=user,
    wrong=wrong
    )

# Login check
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if (user_id != None):
            user = QueryBuilder.singleReadWhere('users', '*', f"UserID={user_id}")
            if (user['Username'] is None):
                return redirect(url_for('login_get'))
        else:
            return redirect(url_for('login_get'))
        return view(**kwargs)
    return wrapped_view

# Home page post route with account and password checker
@app.post('/')
def login_post():
    user = request.form["users"]
    password = request.form["password"]
    try:
        row = QueryBuilder.singleReadWhere('users', '*', f"Username = '{user}'")
        if check_password_hash(row['Password'], password):
            session.clear()
            session['user_id'] = row['UserID']
            return redirect(f"/addService/")
        else:
            session.clear()
            return render_template(
                'login.html',
                title='Login',
                user=user,
                wrong='wrong'
            )
    except Exception as e:
        print(e)
        session.clear()
        return render_template(
            'login.html',
            title='Login',
            user=user,
            wrong='wrong'
            )
        
# Maintenance backend
@app.get('/maintenance')
@login_required
def maintenance():
    post = list_user()
    return render_template('maintenance.html', post=post, row=None)

# Gets full user list
def list_user():
    try:
        post = QueryBuilder.readFromTable('Users', '*')
        return post
    except Exception as e:
        print(e)

# Populates username and password fields
@app.get('/maintenance/<int:id>/edit')
@login_required
def edit(id):
    post = list_user()
    try:
        row = QueryBuilder.singleReadWhere("Users", 'UserID, Username, Password', f"UserID={id}")
        return render_template('maintenance.html', post=post, row=row)
    except:
        post = list_user()
        return render_template('maintenance.html', post=post, row=None)

# Commits changes made to queried user
@app.post('/maintenance/<int:id>')
@login_required
def update_user(id):
    user = request.form['username']
    password = request.form['password']
    print(id)
    try:
        QueryBuilder.updateTable('Users', f"Username='{user}', Password='{generate_password_hash(password)}'", f"UserID={id}")
        print('password' == check_password_hash(password))
        return redirect(url_for('maintenance'))
    except:
        return redirect(url_for('maintenance'))

# Removes current session
@app.get('/logout')
def logout_user():
    session.clear()
    return redirect(url_for('login_get'))