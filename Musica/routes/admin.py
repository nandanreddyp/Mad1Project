from Musica import app
from .permissions import allowed_for

from functools import wraps
from Musica.database.models import *
from Musica.functions import *
from flask import session, render_template, flash, redirect, url_for, request

##Admin Main Page##
###################
@app.route('/admin', methods=['GET', 'POST'])
@allowed_for(['admin'])
def admin_home():
    session['currentPage'] = 'admin_home'
    count = {
        'users'   : User.query.filter(User.role=='user').count(),
        'premium' : User.query.filter(User.premium==True).count(),
        'admins'  : User.query.filter(User.role=='admin').count(),
        'creators': User.query.filter(User.role=='creator').count(),
        'blacklist': User.query.filter(User.blacklist).count(),
        'total_users'   : User.query.count(),
        'songs'   : Song.query.count(),
        'flagged_songs': Song.query.filter(Song.flagged==True).count(),
        'albums'  : Album.query.count(),
        'flagged_albums': Album.query.filter(Album.flagged==True).count(),
        }
    popular = Song.query.filter(Song.flagged==False).order_by(Song.play_count.desc()).limit(3)
    # show no of users, creators; no of songs, albums; top 3 trending song
    return render_template('admin/home.html',count=count,popular=popular)

##Premium Requests##
@app.route('/admin/premium_requests/', defaults={'req_id': None, 'action': None}, methods=['GET', 'POST'])
@app.route('/admin/premium_requests/<int:req_id>/<action>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def premium_requests(req_id,action):
    session['currentPage'] = 'premium_req'
    req = PremiumReq.query.get(req_id)
    if request.method=='GET' and not(action) and not(req_id):
        requests = PremiumReq.query.order_by(PremiumReq.time_added.desc()).all()
        return render_template('admin/premium_req.html',requests=requests)
    elif req and action:
        user = User.query.get(req.user_id)
        if action == 'accept':
            user.premium = True; db.session.delete(req)
            db.session.commit()
            flash('Accepted user request','success')
        elif action == 'reject':
            db.session.delete(req); db.session.commit()
            flash('Rejected user request','success')
    elif request.method == 'POST':
        user_id = request.form.get('user_id')
        results = PremiumReq.query.filter(func.lower(PremiumReq.user_id).ilike(f'%{user_id}%')).all()
        return render_template('admin/premium_req.html',requests=results,filter=True)
    return redirect('/admin/premium_requests')

##Flag song/album##
@app.route('/admin/flagged/')
@allowed_for(['admin'])
def flagged():
    songs = Song.query.filter(Song.flagged==True).all()
    albums = Album.query.filter(Album.flagged==True).all()
    return render_template('admin/sub-temp/flagged.html',songs=songs,albums=albums)

@app.route('/admin/flag',defaults={'category':None,'action':None,'item_id':None,'action':None}, methods=['GET','POST'])
@app.route('/admin/flag/<category>/<int:item_id>/<action>', methods=['GET','POST'])
@allowed_for(['admin'])
def flag(category,item_id,action):
    session['currentPage'] = 'flag_content'
    if not(category and item_id) and not(request.args.get('type')):
        return render_template('admin/flag.html')
    elif request.method == 'GET' and request.args.get('type') and request.args.get('id'):
        item_type = request.args.get('type'); item_id = request.args.get('id')
        if item_type=='song':
            song = Song.query.get(item_id)
            return render_template('admin/flag.html',filter=True,result=song)
        elif item_type=='album':
            album = Album.query.get(item_id)
            return render_template('admin/flag.html',filter=True,result=album)
    if category == 'song':
        song = Song.query.get(item_id)
        if action == 'flag':
            song.flagged = True
            flash('Flagged song','success')
        elif action == 'unflag':
            song.flagged = False
            flash('Unflagged song','success')
        elif action == 'delete':
            if song.cover: remove_file('image/song',song.cover)
            if song.lyrics: remove_file('lyrics',song.lyrics)
            remove_file('song',song.filename)
            db.session.delete(song)
            db.session.commit()
            flash('Song deleted','success')
            return redirect('/admin/flag'); db.session.commit()
        db.session.commit()
        return redirect(f'/admin/flag?type=song&id={item_id}')
    elif category == 'album':
        album = Album.query.get(item_id)
        if action == 'flag':
            album.flagged = True
            flash('Flagged album','success')
        elif action == 'unflag':
            album.flagged = False
            flash('Unflagged album','success')
        elif action == 'delete':
            if album.cover: remove_file('image/album',album.cover)
            db.session.delete(album); db.session.commit()
            flash('Album deleted','success')
            return redirect('/admin/flag')
        db.session.commit()
        return redirect(f'/admin/flag?type=album&id={item_id}')
##Blacklist Creator##
@app.route('/admin/blacklist/', defaults={'way':None}, methods=['GET','POST'])
@app.route('/admin/blacklist/<way>', methods=['GET', 'POST'])
@allowed_for(['admin'])
def blacklist(way):
    session['currentPage'] = 'creator_blacklist'
    from urllib.parse import unquote, quote
    if not(way) and not(request.args.get('user_id')):
        return render_template('admin/creator_blacklist.html')
    elif request.method == 'GET' and request.args.get('user_id') and not(way):
        user = User.query.get(unquote(request.args.get('user_id')))
        return render_template('admin/creator_blacklist.html',creator=user,filter=True)
    elif not(request.args.get('user_id')) and way:
        if way=='view':
            creators = Blacklist.query.order_by(Blacklist.time_added.desc()).all()
            return render_template('admin/sub-temp/blacklist.html',creators=creators)
    elif request.method == 'GET' and request.args.get('user_id') and way:
        user = User.query.get(unquote(request.args.get('user_id')))
        if way == 'add':
            db.session.add(Blacklist(creator_id=user.id)); db.session.commit()
        elif way == 'remove':
            db.session.delete(user.blacklist); db.session.commit()
        return redirect(f'/admin/blacklist/?user_id={user.id}')
    


