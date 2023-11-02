from Musica import app
from .permissions import allowed_for

from functools import wraps
from flask import flash, redirect, url_for, session

# def allowed_for(allowed_roles):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             user_role = session.get('role')
#             if user_role in allowed_roles:
#                 return f(*args, **kwargs)
#             flash('You are not allowed to access this route!', 'warning')
#             return redirect(url_for('home'))
#         return wrapper
#     return decorator

@app.route('/admin', methods=['GET', 'POST'])
@allowed_for(['admin'])
def admin():
    return 'Admin page'



