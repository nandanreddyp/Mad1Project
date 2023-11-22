from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request, send_file

from Musica.routes.permissions import *
from Musica.functions import save_file, remove_file, has_user_liked, update_play_count, update_rating, get_lyrics, get_song, get_linked_list

## Main views ##
################
@app.route('/home')
@login_required
def user_home():
    session['currentPage'] = 'home'
    return render_template('user/home.html')

@app.route('/songs',methods=['GET','POST'])
@login_required
def user_explore():
    session['currentPage'] = 'explore'
    if request.method=='POST':
        view = request.args.get('view',6,type=int)
        data = request.form; song_name = data.get('song'); artist_name = data.get('artist'); language = data.get('language'); genre = data.get('genre'); sort_by = data.get('sortby')
        filtered = Song.query.filter_by(flagged=False)
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
            elif sort_by == 'alphabetical': filtered = filtered.order_by(func.lower(Song.title).asc())
        # filtered = filtered.paginate(page=1, per_page=view)
        filtered = filtered.all()
        flash('Filter applied','success')
        return render_template('user/explore.html',songs=filtered,has_user_liked=has_user_liked,filter=True,view=view+6)
    view = request.args.get('view',6,type=int)
    songs = Song.query.filter_by(flagged=False).order_by(Song.time_added.desc()).paginate(page=1, per_page=view)
    return render_template('user/explore.html',songs=songs,has_user_liked=has_user_liked,view=view+6)

@app.route('/library')
@login_required
def user_library():
    session['currentPage'] = 'library'
    return render_template('user/library.html')

@app.route('/upgrade',methods=['POST','GET'])
@login_required
def get_premium():
    session['currentPage'] = 'upgrade'
    requested = PremiumReq.query.filter_by(user_id=current_user.id).first()
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
@login_required
def songs(song_id):
    song = db.session.get(Song, song_id)
    # song = Song.query.get(song_id)
    if request.method == 'GET' and song:
        if not song.flagged:
            watched = Play.query.filter_by(user_id=current_user.id, song_id=song.id).first()
            if not(watched): db.session.add(Play(user_id=current_user.id, song_id=song.id)); db.session.commit(); update_play_count(song)
            if watched: db.session.delete(watched); db.session.commit(); db.session.add(Play(user_id=current_user.id, song_id=song.id)); db.session.commit()
            return render_template('user/sub-temp/song.html',song=song,get_lyrics=get_lyrics,has_user_liked=has_user_liked)
        else: flash('Song is flagged','info')
    return redirect(url_for('home'))

#rating
@app.route('/songs/<int:song_id>/rate')
@login_required
def rate(song_id):
    song = db.session.get(Song, song_id)
    # song = Song.query.get(song_id)
    if song and not(has_user_liked(current_user,song)):
        db.session.add(Rating(user_id=current_user.id, song_id=song.id)); db.session.commit()
    elif song and has_user_liked(current_user, song):
        rating = Rating.query.filter_by(user_id=current_user.id, song_id=song.id).first()
        db.session.delete(rating); db.session.commit()
    update_rating(song)
    return redirect(f'/songs/{song_id}')

#assign a song to a particular playlist
@app.route('/songs/<int:song_id>/<way>/playlists',defaults={'playlist_id':None},methods=['GET','POST'])
@app.route('/songs/<int:song_id>/<way>/playlists/<int:playlist_id>',methods=['GET','POST'])
@login_required
def from_song_add_playlist(song_id,way,playlist_id):
    song = db.session.get(Song, song_id); playlist = db.session.get(Playlist, playlist_id)
    # song = Song.query.get(song_id); playlist = Playlist.query.get(playlist_id)
    if song and not(playlist) and request.method=='GET':
        playlists=Playlist.query.filter_by(user_id=current_user.id).order_by(Playlist.time_added.desc()).all()
        return render_template('user/sub-temp/song~add-rem.html',albums=playlists,song=song)
    elif song and not(playlist) and request.method=='POST':
        data = request.form; playlist_name = data.get('album'); sort_by = data.get('sortby')
        filtered = Playlist.query.filter_by(user_id=current_user.id)
        if playlist_name:
            filtered = filtered.filter(Playlist.title.ilike('%'+playlist_name+'%'))
        if sort_by:
            if sort_by == 'new': filtered = filtered.order_by(Playlist.time_added.desc())
            elif sort_by == 'old': filtered = filtered.order_by(Playlist.time_added.asc())
            elif sort_by == 'alphabetical': filtered = filtered.order_by(Playlist.title.asc())
        filtered = filtered.all()
        flash('Filter applied','success')
        return render_template('user/sub-temp/song~add-rem.html',song=song,albums=filtered,filter=True)
    elif playlist and song and way:
        if way=='add' and song not in playlist.songs:
            playlist.songs.append(song); db.session.commit()
            flash('Added song to playlist','success')
            return redirect(f'/songs/{song_id}/add/playlists')
        elif way=='remove' and song in playlist.songs:
            playlist.songs.remove(song); db.session.commit()
            flash('Removed song from playlist','success')
            fromm = request.args.get('from',None)
            if not(fromm): return redirect(f'/songs/{song_id}')
            else: return redirect(f'/songs/{song_id}/add/playlists')
    return redirect(f'/songs/{song_id}')

##Album routes##
################
#read
@app.route('/albums', defaults={'album_id':None}, methods=['GET','POST'])
@app.route('/albums/<int:album_id>', methods=['GET','POST'])
@login_required
def albums(album_id):
    session['currentPage'] = 'explore'
    album = db.session.get(Album, album_id)
    # album = Album.query.get(album_id)
    if request.method == 'GET' and album:
        current_ind = request.args.get('play',1,type=int)
        head = get_linked_list(album.songs)
        if current_ind==1 or not(current_ind in range(1,len(album.songs)+1)): current=head
        else:
            for i in range(len(album.songs)):
                current = head.next
                if current_ind == i+2:
                    break
                head = head.next
        return render_template('user/sub-temp/album.html',album=album,current=current,get_lyrics=get_lyrics,has_user_liked=has_user_liked)
    elif request.method == 'POST' and not(album_id):
        data = request.form; album_name = data.get('album'); artist_name = data.get('artist'); sort_by = data.get('sortby')
        filtered = Album.query.filter_by(flagged=False)
        if album_name:
            filtered = filtered.filter(Album.title.ilike('%'+album_name+'%'))
        if artist_name:
            filtered = filtered.filter(Album.artist.ilike('%'+artist_name+'%'))
        if sort_by:
            if sort_by == 'new': filtered = filtered.order_by(Album.time_added.desc())
            elif sort_by == 'old': filtered = filtered.order_by(Album.time_added.asc())
            elif sort_by == 'alphabetical': filtered = filtered.order_by(func.lower(Album.title).asc())
        filtered = filtered.all()
        flash('Filter applied','success')
        return render_template('user/sub-temp/albums.html', albums=filtered, filter=True)
    else :
        albums = Album.query.filter_by(flagged=False).order_by(Album.time_added.desc()).all()
        return render_template('user/sub-temp/albums.html', albums=albums)

#assign album to library
@app.route('/albums/<int:album_id>/<way>/library')
@login_required
def album_to_library(album_id,way):
    album = db.session.get(Album, album_id)
    # album = Album.query.get(album_id)
    if album and way=='add':
        if album not in current_user.library.albums:
            current_user.library.albums.append(album); db.session.commit()
            flash('Song added to library','success')
    elif album and way=='remove':
        if album in current_user.library.albums:
            current_user.library.albums.remove(album); db.session.commit()
            flash('Song removed from library','success')
            return redirect(f'/library/albums')
    return redirect(f'/albums/{album_id}')


##Playlist routes##
###################
#create
@app.route('/playlists/create',methods=['GET','POST'])
@login_required
def create_playlist():
    if request.method == 'GET':
        return render_template('user/sub-temp/playlist-create.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        playlist = Playlist(title=title,user_id=current_user.id)
        db.session.add(playlist)
        current_user.library.playlists.append(playlist)
        db.session.commit()
        return redirect('/library/playlists')
#read
@app.route('/playlists/<int:playlist_id>',methods=['GET','POST'])
@login_required
def playlists(playlist_id):
    if request.method == 'GET' and playlist_id:
        playlist = db.session.get(Playlist, playlist_id)
        # playlist = Playlist.query.get(playlist_id)
        if playlist.user_id == current_user.id:
            current_ind = request.args.get('play',1,type=int)
            head = get_linked_list(playlist.songs)
            if current_ind==1 or not(current_ind in range(1,len(playlist.songs)+1)): current=head
            else:
                for i in range(len(playlist.songs)):
                    current = head.next
                    if current_ind == i+2:
                        break
                    head = head.next
            return render_template('user/sub-temp/playlist.html',album=playlist,current=current,get_lyrics=get_lyrics,has_user_liked=has_user_liked)
        return redirect(url_for('creator_home'))
    elif request.method == 'POST':
        # return filtered results
        pass
    else :
        playlists = Playlist.query.filter_by(Playlist.user_id==current_user.id).all()
        return render_template('creator/playlists.html', playlists=playlists)
#update
@app.route('/playlists/<int:playlist_id>/<method>',methods=['GET','POST'])
@login_required
def playlist_edit(playlist_id,method):
    playlist = db.session.get(Playlist, playlist_id)
    # playlist = Playlist.query.get(playlist_id)
    if playlist and method=='update' and playlist.user_id==current_user.id:
        if request.method == 'GET':
            return render_template('user/sub-temp/playlist-create.html',playlist=playlist)
        elif request.method == 'POST':
            title = request.form.get('title')
            playlist.title=title
            db.session.commit()
            flash('Updated playlist details','success')
            return redirect(f'/playlists/{playlist_id}')
        return redirect(f'/playlists/{playlist_id}')
    elif playlist and method=='delete' and playlist.user_id==current_user.id:
        db.session.delete(playlist); db.session.commit()
        flash('Successfully deleted playlist','success')
    return redirect('/library/playlists')

#assign a playlist a particular song
@app.route('/playlists/<int:playlist_id>/<way>/songs',defaults={'song_id':None},methods=['GET','POST'])
@app.route('/playlists/<int:playlist_id>/<way>/songs/<int:song_id>',methods=['GET','POST'])
@login_required
def from_playlist_add_song(playlist_id,way,song_id):
    playlist = db.session.get(Playlist, playlist_id); song = db.session.get(Song, song_id)
    # playlist = Playlist.query.get(playlist_id); song = Song.query.get(song_id)
    if way=='add' and playlist and song:
        if song not in playlist.songs:
            playlist.songs.append(song); db.session.commit()
            flash('Added song into playlist','success')
            return redirect(f'/playlists/{playlist_id}/add/songs')
    elif way=='remove' and playlist and song:
        if song in playlist.songs:
            playlist.songs.remove(song); db.session.commit()
            flash('Removed song from playlist','success')
            fromm = request.args.get('from',None)
            if not(fromm):
                return redirect(f'/playlists/{playlist_id}')
            return redirect(f'/playlists/{playlist_id}/add/songs')
    elif playlist and not(song) and request.method=='GET':
        view = request.args.get('view',6,type=int)
        songs = Song.query.order_by(Song.time_added.desc()).paginate(page=1, per_page=view) 
        return render_template('user/sub-temp/playlist~add-rem.html',playlist=playlist,songs=songs,view=view+6)
    elif playlist_id and not(song_id) and request.method=='POST':
        view = request.args.get('view',6,type=int)
        data = request.form; song_name = data.get('song'); artist_name = data.get('artist'); language = data.get('language'); genre = data.get('genre'); sort_by = data.get('sortby')
        filtered = Song.query
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
        return render_template('user/sub-temp/playlist~add-rem.html',playlist=playlist,songs=filtered,filter=True,view=view+6)
    return redirect(f'/playlists/{playlist_id}')

##Library routes##
##################
@app.route('/library/<item>')
@login_required
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
    playlists = Playlist.query.filter(Playlist.title.ilike(f'%{query}%'),Playlist.user_id==current_user.id).all()
    return render_template('user/sub-temp/search.html',songs=songs,albums=albums,playlists=playlists,query=query,has_user_liked=has_user_liked)

@app.route('/download/<int:song_id>')
@login_required
@premium_required
def download(song_id):
    song = db.session.get(Song, song_id)
    # song = Song.query.get(song_id)
    file_path = get_song(song.filename)
    filename = song.title +'.'+ song.filename.split('.')[-1]
    return send_file(file_path,download_name=filename,as_attachment=True)
