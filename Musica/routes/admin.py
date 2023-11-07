from Musica import app
from .permissions import allowed_for

from functools import wraps
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

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


##Admin Main Page##
###################
@app.route('/admin', methods=['GET', 'POST'])
@allowed_for(['admin'])
def admin():
    # show no of users, creators; no of songs, albums; top 3 trending song
    return 'Admin page'

##Premium Requests##
@app.route('/admin/premium_requests/<status>/<user_id>/<action>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def premium_requests(status,user_id,action):
    if request.method=='GET':
        if status == 'pending':
            # show all pending and perform action
            pass
        elif status == 'completed':
            # show all completed and perform action
            pass
        #show all requests
        pass
    elif request.method=='POST':
        #update premium
        pass
##Blacklist Creator##
@app.route('/admin/blacklist/<way>/<user_id>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def blacklist(way,user_id):
    if request.method=='GET':
        #show all flagged or queried
        pass
    elif request.method=='POST':
        if way=='add':
            #add creator to flagged
            pass
        elif way=='remove':
            #remove creator from flagged
            pass
##Flag song/album##
@app.route('/admin/flagged/<category>/<method>/<int:item_id>', methods=['GET','POST'])
@allowed_for(['admin'])
def flag(category,method,item_id):
    if category == 'songs':
        if not(method):
            #show flagged items
            pass
        elif method == 'add':
            # add to flagged
            pass
        elif method == 'remove':
            #remove from flagged
            pass
    elif category == 'albums':
        if not(method):
            #show flagged items
            pass
        elif method == 'add':
            # add to flagged
            pass
        elif method == 'remove':
            #remove from flagged
            pass


    


