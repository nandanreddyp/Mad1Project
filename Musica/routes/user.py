from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request, send_file

from Musica.routes.permissions import *
from Musica.functions import save_file, remove_file, has_user_liked, update_play_count, update_rating, get_lyrics, get_song

## Main views ##
################
@app.route('/home')
@login_required
def user_home():
    session['currentPage'] = 'home'
    return render_template('user/home.html')

@app.route('/songs',methods=['GET','POST'])
def user_explore():
    session['currentPage'] = 'explore'
    if request.method=='POST':
        view = request.args.get('view',6,type=int)
        data = request.form; song_name = data.get('song'); artist_name = data.get('artist'); language = data.get('language'); genre = data.get('genre'); sort_by = data.get('sortby')
        filtered = Song.query.filter_by(user_id=current_user.id)
        if song_name:
            filtered = filtered.filter(Song.title.ilike('%'+song_name+'%'))
        if artist_name:
            filtered = filtered.filter(Song.artist.ilike('%'+artist_name+'%'))
        if language:
            filtered = filtered.filter(Song.language.ilike('%'+language+'%'))
        if genre:
            filtered =  filtered.filter(Song.genre.ilike('%'+genre+'%'))
        if sort_by:
            if sort_by == 'new': filtered = filtered.order_by(Song.time_added.desc())
            elif sort_by == 'old': filtered = filtered.order_by(Song.time_added.asc())
            elif sort_by == 'rating_high': filtered = filtered.order_by(Song.rating.desc())
            elif sort_by == 'rating_low': filtered = filtered.order_by(Song.rating.asc())
            elif sort_by == 'alphabetical': filtered = filtered.order_by(Song.title.asc())
        filtered = filtered.paginate(page=1, per_page=view)
        flash('Filter applied','success')
        return render_template('user/explore.html',songs=filtered,has_user_liked=has_user_liked,filter=True,view=view+6)
    view = request.args.get('view',6,type=int)
    songs = Song.query.filter_by(flagged=False).order_by(Song.time_added.desc()).paginate(page=1, per_page=view)
    return render_template('user/explore.html',songs=songs,has_user_liked=has_user_liked,view=view+6)

@app.route('/library')
def user_library():
    session['currentPage'] = 'library'
    return render_template('user/library.html')

@app.route('/upgrade',methods=['POST','GET'])
def get_premium():
    session['currentPage'] = 'upgrade'
    requested = PremiumReq.query.get(current_user.id)
    if request.method == 'GET':
        if requested: flash('You already requested, you can update transaction id','info')
        return render_template('user/upgrade.html',requested=requested)
    elif current_user.premium != True and request.method == 'POST':
        trans_id = request.form.get('transaction_id')
        if requested: requested.trans_id = trans_id; flash('Updated transaction id','success')
        else: new_request = PremiumReq(user_id=current_user.id, trans_id=trans_id); db.session.add(new_request); flash('Premium request successfully created','success')
        db.session.commit()
    return redirect(url_for('user_home'))


##Song routes##
###############
#read
@app.route('/songs/<int:song_id>')
def songs(song_id):
    song = Song.query.get(song_id)
    if request.method == 'GET' and song:
        watched = Play.query.filter_by(user_id=current_user.id, song_id=song.id).first()
        if not(watched): db.session.add(Play(user_id=current_user.id, song_id=song.id)); db.session.commit(); update_play_count(song)
        return render_template('user/sub-temp/song.html',song=song,get_lyrics=get_lyrics,has_user_liked=has_user_liked)

#rating
@app.route('/songs/<int:song_id>/rate')
def rate(song_id):
    song = Song.query.get(song_id)
    if song and not(has_user_liked(current_user,song)):
        db.session.add(Rating(user_id=current_user.id, song_id=song.id)); db.session.commit()
    elif song and has_user_liked(current_user, song):
        rating = Rating.query.filter_by(user_id=current_user.id, song_id=song.id).first()
        db.session.delete(rating); db.session.commit()
    update_rating(song)
    return redirect(f'/songs/{song_id}')

#assign a song to a particular playlist
@app.route('/songs/<int:song_id>/<way>/playlists/<int:playlist_id>')
def from_song_add_playlist(song_id,way,playlist_id):
    song = Song.query.get(song_id); playlist = Playlist.query.get(playlist_id)
    if playlist_id and not(song_id) and request.method=='GET':
        # show not added user playlists in pagination format
        pass
    elif playlist_id and not(song_id) and request.method=='POST':
        # show filtered not added user playlists in pagination format
        pass
    elif playlist_id and song_id and request.method=='POST':
        # add song in playlist
        pass
    else:
        flash('Error while adding song into playlist','error')
        return redirect(url_for('home'))

##Album routes##
################
#read
@app.route('/albums', defaults={'album_id':None}, methods=['GET','POST'])
@app.route('/albums/<int:album_id>', methods=['GET','POST'])
def albums(album_id):
    session['currentPage'] = 'explore'
    album = Album.query.get(album_id)
    if request.method == 'GET' and album:
        return render_template('user/album_view.html',album=album)
    elif request.method == 'POST' and not(album_id):
        data = request.form; album_name = data.get('album'); artist_name = data.get('artist'); sort_by = data.get('sortby')
        filtered = Album.query.filter_by(user_id=current_user.id)
        if album_name:
            filtered = filtered.filter(Album.title.ilike('%'+album_name+'%'))
        if artist_name:
            filtered = filtered.filter(Album.artist.ilike('%'+artist_name+'%'))
        if sort_by:
            if sort_by == 'new': filtered = filtered.order_by(Album.time_added.desc())
            elif sort_by == 'old': filtered = filtered.order_by(Album.time_added.asc())
            elif sort_by == 'alphabetical': filtered = filtered.order_by(Album.title.asc())
        filtered = filtered.all()
        flash('Filter applied','success')
        return render_template('user/sub-temp/albums.html', albums=filtered, filter=True)
    else :
        albums = Album.query.filter_by(flagged=False).all()
        return render_template('user/sub-temp/albums.html', albums=albums)

#assign album to library
@app.route('/albums/<int:album_id>/<way>/library')
def album_to_library(album_id,way):
    album = Song.query.get(album_id)
    if album and way=='add':
        if album not in current_user.library.albums:
            current_user.library.albums.append(album); db.session.commit()
            flash('Song added to library','success')
    elif album and way=='remove':
        if album in current_user.library.albums:
            current_user.library.albums.remove(album); db.session.commit()
            flash('Song removed from library','success')
    return redirect(f'/albums/{album_id}')


##Playlist routes##
###################
#create
@app.route('/playlists/create',methods=['GET','POST'])
def create_playlist():
    if request.method == 'GET':
        return render_template('user/sub-temp/playlist-create.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        playlist = Playlist(title=title,user_id=current_user.id)
        db.session.add(playlist)
        current_user.library.playlists.append(playlist)
        db.session.commit()
        return redirect('/library')
#read
@app.route('/playlists/<int:playlist_id>',methods=['GET','POST'])
def playlists(playlist_id):
    if request.method == 'GET' and playlist_id:
        playlist = Playlist.query.get(playlist_id)
        if playlist.user_id == session['user_id']:
            return render_template('creator/playlist_view.html',playlist=playlist)
        return redirect(url_for('creator_home'))
    elif request.method == 'POST':
        # return filtered results
        pass
    else :
        playlists = Playlist.query.filter_by(Playlist.user_id==session['user_id']).all()
        return render_template('creator/playlists.html', playlists=playlists)
#update
@app.route('/playlists/<int:playlist_id>/<method>',methods=['GET','POST'])
def playlist_edit(playlist_id,method):
    playlist = Playlist.query.get(playlist_id)
    if playlist and method=='update' and playlist.user_id==current_user.id:
        if request.method == 'GET':
            return render_template('user/sub-temp/playlist-create.html',playlist=playlist)
        elif request.method == 'POST':
            title = request.form.get('title')
            playlist.title=title
            db.session.commit()
            return redirect('/library/playlists')
        return redirect(f'/playlists/{playlist_id}')
    elif playlist and method=='delete' and playlist.user_id==current_user.id:
        db.session.delete(playlist); db.session.commit()
        flash('Successfully deleted playlist','success')
    return redirect('/library/playlists')

#assign a playlist a particular song
@app.route('/playlists/<int:playlist_id>/<way>/songs',defaults={'song_id':None},methods=['GET','POST'])
@app.route('/playlists/<int:playlist_id>/<way>/songs/<int:song_id>',methods=['GET','POST'])
def from_playlist_add_song(playlist_id,song_id):
    playlist = Playlist.query.get(playlist_id); song = Song.query.get(song_id)
    if way=='add':
        if playlist and song:
            if playlist.user_id != current_user.id:
                flash('Not your playlist to add song!','warning')
                return redirect(f'/playlists/{playlist_id}')
            elif song not in playlist.songs:
                playlist.songs.append(song); db.session.commit()
                flash('Added song into playlist','success')
                return redirect(f'/playlists/{playlist_id}/add/songs')
    elif way=='remove':
        if playlist and song:
            if playlist.user_id != current_user.id:
                flash('Not your playlist to remove song!','warning')
                return redirect(f'/playlists/{playlist_id}')
            elif song in playlist.songs:
                playlist.songs.remove(song); db.session.commit()
                flash('Removed song from playlist','success')
                return redirect(f'/playlists/{playlist_id}/add/songs')
    elif playlist and not(song) and request.method=='GET':
        # show not added user songs in pagination format
        pass
    elif playlist_id and not(song_id) and request.method=='POST':
        # show filtered not added user songs in pagination format
        pass
    return redirect(f'/playlists/{playlist_id}')

##Library routes##
##################
@app.route('/library/<item>')
def library_view_item(item):
    session['currentPage']='library'
    if item=='albums':
            return render_template('user/sub-temp/lib-albums.html')
    elif item=='playlists':
            return render_template('user/sub-temp/lib-playlists.html')
    return redirect('/library')

### others ###

@app.route('/history',methods=['get'])
@login_required
def history():
    session['currentPage'] = None
    songs = [x.song for x in current_user.played]
    return render_template('user/sub-temp/history.html',songs=songs,has_user_liked=has_user_liked)

@app.route('/profile',methods=['get','post'])
@login_required
def profile():
    session['currentPage'] = None
    if request.method == 'POST':
        data = request.form; file = request.files.get('dp')
        current_user.f_name = data['f_name']; current_user.l_name = data['l_name']
        delete = data.get('delete_dp')
        if file and not(delete):
            image_loc = save_file('image/profile',current_user.id,file)
            current_user.cover=image_loc
        if current_user.cover and delete:
            remove_file('image/profile',current_user.cover)
            current_user.cover=None
        db.session.commit()
        flash('Updated your profile','success')
        return redirect(url_for('user_home'))
    return render_template('user/sub-temp/profile.html')

@app.route('/search',methods=['get','post'])
@login_required
def search():
    session['currentPage'] =  None
    query = request.args.get('query')
    songs = Song.query.filter(or_(Song.title.ilike(f'%{query}%'),Song.artist.ilike(f'%{query}%'))).all()
    albums = Album.query.filter(or_(Album.title.ilike(f'%{query}%'),Album.artist.ilike(f'%{query}%'))).all()
    playlists = Playlist.query.filter(Playlist.title.ilike(f'%{query}%')).all()
    return render_template('user/sub-temp/search.html',songs=songs,albums=albums,playlists=playlists,query=query,has_user_liked=has_user_liked)

@app.route('/download/<int:song_id>')
@login_required
def download(song_id):
    song = Song.query.get(song_id)
    file_path = get_song(song.filename)
    filename = song.title +'.'+ song.filename.split('.')[-1]
    print(filename)
    return send_file(file_path,download_name=filename,as_attachment=True)
