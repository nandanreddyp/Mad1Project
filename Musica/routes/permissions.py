from functools import wraps
from flask import redirect, url_for, flash, session
from .welcome import current_user

from functools import wraps

def login_not_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated:
            flash('You are already loggedin!','info')
            return redirect(url_for('home'))
        return f(*args,**kwargs)
    return wrapper

def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        flash('Welcome to Musica, login or signup to enter...','info')
        return redirect(url_for('welcome'))
    return wrapper

def allowed_for(list):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args,**kwargs):
            if current_user.role in list:
                    return f(*args,**kwargs)
            flash('You are not allowed to access this route!','warning')
            return redirect(url_for('home'))
        return wrapper
    return decorator

def not_in_blacklist(f):
    @wraps(f)
    @login_required
    def wrapper(*args,**kwargs):
        if current_user.blacklist:
            flash('You are in blacklist for breaching policies, contact admin for more details.','warning')
            return redirect(url_for('home'))
        return f(*args,**kwargs)
    return wrapper

def premium_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args,**kwargs):
        if not current_user.premium:
            flash('Get premium in upgrade section','info')
            flash('You are not premium user!','warning')
            return redirect(url_for('user_home'))
        return f(*args,**kwargs)
    return wrapper
