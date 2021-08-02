# Reference from : https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/
from functools import wraps
from flask import session, flash, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You have NOT permission. Please log in.', 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function