from Musica import app
from .permissions import allowed_for

from functools import wraps
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

##Admin Main Page##
###################
@app.route('/admin', methods=['GET', 'POST'])
@allowed_for(['admin'])
def admin_home():
    session['currentPage'] = 'admin_home'
    # show no of users, creators; no of songs, albums; top 3 trending song
    return render_template('admin/home.html')

##Premium Requests##
@app.route('/admin/premium_requests/', defaults={'status': None, 'user_id': None, 'action': None}, methods=['GET', 'POST'])
@app.route('/admin/premium_requests/<status>/<user_id>/<action>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def premium_requests(status,user_id,action):
    session['currentPage'] = 'premium_req'
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
    return render_template('admin/premium_req.html')
##Flag song/album##
@app.route('/admin/flagged/',defaults={'category':None,'method':None,'item_id':None}, methods=['GET','POST'])
@app.route('/admin/flagged/<category>/<method>/<int:item_id>', methods=['GET','POST'])
@allowed_for(['admin'])
def flag(category,method,item_id):
    session['currentPage'] = 'flag_content'
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
    return render_template('admin/flag.html')
##Blacklist Creator##
@app.route('/admin/blacklist/', defaults={'way':None, 'user_id':None}, methods=['GET','POST'])
@app.route('/admin/blacklist/<way>/<user_id>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def blacklist(way,user_id):
    session['currentPage'] = 'creator_blacklist'
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
    return render_template('admin/creator_blacklist.html')
    


