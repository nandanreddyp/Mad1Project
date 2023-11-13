from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

from Musica.routes.permissions import *
from Musica.functions import save_file, remove_file

## Main views ##
################
@app.route('/home')
@login_required
def user_home():
    session['currentPage'] = 'home'
    return render_template('user/home.html')

@app.route('/explore')
def user_explore():
    session['currentPage'] = 'explore'
    return render_template('user/explore.html')

@app.route('/library')
def user_library():
    session['currentPage'] = 'library'
    return render_template('user/library.html')

@app.route('/upgrade')
def get_premium():
    session['currentPage'] = 'upgrade'
    if request.method == 'GET':
        return render_template('user/upgrade.html')
    current_user = User.query.get(session['user_id'])
    if current_user and current_user.premium != True and request.method == 'POST':
        # make a premium request
        flash('Premium request successfully created','success')
    else:
        flash('You are already Premium user!','info')
    return redirect(url_for('user_home'))


##Song routes##
###############
#read
@app.route('/songs/', defaults={'song_id':None}, methods=['GET','POST'])
@app.route('/songs/<int:song_id>',methods=['GET','POST'])
def uploads(song_id):
    if request.method == 'GET' and song_id:
        song = Song.query.get(song_id)
        return render_template('user/sub-temp/rating.html')
    elif request.method == 'POST':
        # return queried results
        pass
    else:
        # show all songs
        songs = Song.query.filter_by(Song.user_id==current_user.id).all()
        return render_template('creator/songs.html', songs=songs)
#rating with json to update without increment count
@app.route('/songs/<int:song_id>/rate/<int:rating>')
def rate(song_id,rating):
    pass
#assign a song to a particular playlist
@app.route('/songs/<int:song_id>/add/<int:playlist_id>')
def from_song_add_playlist(song_id,playlist_id):
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
@app.route('/albums/<int:album_id>',methods=['GET','POST'])
def albums(album_id):
    if request.method == 'GET' and album_id:
        album = Album.query.get(album_id)
        return render_template('creator/album_view.html',album=album)
    elif request.method == 'POST':
        # return filtered results
        pass
    else :
        albums = Album.query.filter_by(Album.user_id==session['user_id']).all()
        return render_template('creator/albums.html', albums=albums)

##Playlist routes##
###################
#create
@app.route('/playlists/create',methods=['GET','POST'])
def create_playlist():
    if request.method == 'GET':
        pass
        # send form to upload
    elif request.method == 'POST':
        pass
        # make song data in db and save file
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
@app.route('/playlists/<int:playlist_id>/update',methods=['GET','POST'])
def playlist_edit(playlist_id):
    if request.method == 'GET':
        playlist = Playlist.query.get(playlist_id)
        return render_template('creator/playlist_update.html',playlist=playlist)
    elif request.method == 'POST':
        # update song details
        pass
    pass
#delete
@app.route('/playlists/<int:playlist_id>/delete')
def delete(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist_id and playlist:
        db.session.delete(playlist); db.session.commit()
        # remove file in uploads also
        flash('Successfully deleted playlist','success')
        return redirect('/playlists')
    else:
        flash('Error deleting playlist!','error')
        return redirect('/playlists')
#assign a playlist a particular song
@app.route('/playlists/<int:playlist_id>/add/<int:song_id>')
def from_playlist_add_song(playlist_id,song_id):
    playlist = Playlist.query.get(playlist_id); song = Song.query.get(song_id)
    if playlist.user_id != session['user_id']:
        flash('Not your playlist to add song!','warning')
        return redirect(url_for('creator_home'))
    if playlist_id and not(song_id) and request.method=='GET':
        # show not added user songs in pagination format
        pass
    elif playlist_id and not(song_id) and request.method=='POST':
        # show filtered not added user songs in pagination format
        pass
    elif playlist_id and song_id and request.method=='POST':
        # add song in playlist
        pass
    else:
        flash('Error while adding song into playlist','error')
        return redirect(url_for('creatorhome'))
#remove song from playlist
@app.route('/creator/playlists/<int:playlist_id>/remove/<int:song_id>')
def from_playlist_remove_song(playlist_id,song_id):
    playlist = Playlist.query.get(playlist_id); song = Song.query.get(song_id)
    if playlist.user_id != session['user_id']:
        flash('Not your playlist to add song!','warning')
        return redirect(url_for('creator_home'))
    if song in playlist.songs:
        playlist.songs.remove(song)
        flash('Removed song from playlist','success')
    else:
        flash('Song not in playlist to remove!','warning')
    return redirect(f'/creator/playlists/{playlist_id}')

##Library routes##
##################
#songssssssssssssssssssssssssssssssssssssssssssssssss
@app.route('/library/songs')
def library_songs():
    # show songs in library
    pass
@app.route('/library/songs/add/<int:song_id>')
def library_add_song():
    # add song in library
    pass
@app.route('/library/songs/remove/<int:song_id>')
def library_remove_song():
    # remove song
    pass
#albumsssssssssssssssssssssssssssssssssssssssssssssss
@app.route('/library/albums')
def library_albums():
    # show albums in library
    pass
@app.route('/library/albums/add/<int:album_id>')
def library_add_album():
    # add album in library
    pass
@app.route('/library/albums/remove/<int:album_id>')
def library_remove_album():
    # remove album
    pass
#playlistssssssssssssssssssssssssssssssssssssssssssss
@app.route('/library/playlists')
def library_playlists():
    # show playlists in library
    pass
@app.route('/library/playlists/add/<int:playlist_id>')
def library_add_playlist():
    # add playlist in library if public
    pass
@app.route('/library/playlists/remove/<int:playlist_id>')
def library_remove_playlist():
    # remove playlist
    pass

### others ###
@app.route('/profile',methods=['get','post'])
def profile():
    session['currentPage'] = None
    if request.method == 'POST':
        data = request.form; file = request.files.get('dp')
        current_user.f_name = data['f_name']; current_user.l_name = data['l_name']
        delete = data.get('delete_dp')
        if file and not(delete):
            image_loc = save_file('image/profile',current_user.id,file)
            current_user.cover=image_loc
            db.session.commit()
        if current_user.cover and delete:
            remove_file('image/profile',current_user.cover)
            current_user.cover=None
            db.session.commit()
    return render_template('user/sub-temp/profile.html')