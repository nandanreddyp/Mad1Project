from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

from Musica.routes.permissions import *


##Become Creator##
##################
@app.route('/get_creator_role',methods=['GET','post'])
@login_required
def become_creator():
    if request.method == 'GET' and current_user.role!='creator':
        return render_template('user/sub-temp/creator.html')
    elif current_user.role != 'creator' and request.method == 'POST':
        current_user.role = 'creator'; db.session.commit()
        flash('You are now creator!','success')
    return redirect(url_for('creator_home'))

##Creator Main Page routes##
##############################################################################################################################

@app.route('/creator')
@allowed_for(['creator'])
@not_in_blacklist
def creator_home():
    session['currentPage']='creator_home'
    # show info about trending songs, albums
    return render_template('creator/home.html')
    
@app.route('/creator/uploads/upload',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def upload():
    session['currentPage']='upload'
    if request.method == 'GET':
        pass
        # send form to upload
    elif request.method == 'POST':
        pass
        # make song data in db and save file
    return render_template('creator/upload.html')

@app.route('/creator/uploads/', defaults={'song_id': None}, methods=['GET', 'POST'])
@app.route('/creator/uploads/<int:song_id>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def all_uploads(song_id):
    session['currentPage']='uploads'
    # if request.method == 'GET' and song_id:
    #     song = Song.query.get(song_id)
    #     if song.user_id == session['user_id']:
    #         return render_template('creator/song_view.html',song=song)
    #     return redirect(url_for('creator_home'))
    # elif request.method == 'POST':
    #     # return queried results
    #     pass
    # else:
    #     songs = Song.query.filter_by(Song.user_id==session['user_id']).all()
    #     return render_template('creator/songs.html', songs=songs)
    return render_template('creator/uploads.html')

@app.route('/creator/albums/', defaults={'album_id': None}, methods=['GET', 'POST'])
@app.route('/creator/albums/<int:album_id>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def albums_creator(album_id):
    session['currentPage']='albums'
    # if request.method == 'GET' and album_id:
    #     album = Album.query.get(album_id)
    #     if album.user_id == session['user_id']:
    #         return render_template('creator/album_view.html',album=album)
    #     return redirect(url_for('creator_home'))
    # elif request.method == 'POST':
    #     # return filtered results
    #     pass
    # else :
    #     albums = Album.query.filter_by(Album.user_id==session['user_id']).all()
    #     return render_template('creator/albums.html', albums=albums)        
    return render_template('creator/albums.html')

##Song routes##
##############################################################################################################################
#update
@app.route('/creator/uploads/<int:song_id>/update',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def upload_edit(song_id):
    if request.method == 'GET':
        song = Song.query.get(song_id)
        return render_template('creator/song_update.html',song=song)
    elif request.method == 'POST':
        # update song details
        pass
    pass
#delete
@app.route('/creator/uploads/<int:song_id>/delete')
@allowed_for(['creator'])
@not_in_blacklist
def upload_delete(song_id):
    song = Song.query.get(song_id)
    if song_id and song:
        db.session.delete(song); db.session.commit()
        # remove file in uploads also
        flash('Successfully deleted song','success')
        return redirect('/uploads')
    else:
        flash('Error deleting song!','error')
        return redirect('/uploads')
#assign a song to a particular album
@app.route('/creator/uploads/<int:song_id>/add/<int:album_id>')
@allowed_for(['creator'])
@not_in_blacklist
def from_song_add_album(song_id,album_id):
    song = Song.query.get(song_id); album = Album.query.get(album_id)
    if album_id and not(song_id) and request.method=='GET':
        # show not added user albums in pagination format
        pass
    elif album_id and not(song_id) and request.method=='POST':
        # show filtered not added user albums in pagination format
        pass
    elif album_id and song_id and request.method=='POST':
        # add song in album
        pass
    else:
        flash('Error while adding song into album','error')
        return redirect(url_for('creatorhome'))


##Album routes##
################
#create
@app.route('/creator/albums/create',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def create_album():
    if request.method == 'GET':
        pass
        # send form to upload
    elif request.method == 'POST':
        pass
        # make song data in db and save file
#update
@app.route('/creator/albums/<int:album_id>/update',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def album_edit(album_id):
    if request.method == 'GET':
        album = Album.query.get(album_id)
        return render_template('creator/album_update.html',album=album)
    elif request.method == 'POST':
        # update song details
        pass
    pass
#delete
@app.route('/creator/albums/<int:album_id>/delete')
@allowed_for(['creator'])
@not_in_blacklist
def album_delete(album_id):
    album = Album.query.get(album_id)
    if album_id and album:
        db.session.delete(album); db.session.commit()
        # remove file in uploads also
        flash('Successfully deleted album','success')
        return redirect('/albums')
    else:
        flash('Error deleting album!','error')
        return redirect('/albums')
#assign a album a particular song
@app.route('/creator/albums/<int:album_id>/add/<int:song_id>')
@allowed_for(['creator'])
@not_in_blacklist
def from_album_add_song(album_id,song_id):
    album = Album.query.get(album_id); song = Song.query.get(song_id)
    if album_id: 
        if album is None or album.user_id != session['user_id']: 
            flash('Not your album to add song!','warning')
            return redirect(url_for('creator_home'))
    if album_id and not(song_id) and request.method=='GET':
        # show not added user songs in pagination format
        pass
    elif album_id and not(song_id) and request.method=='POST':
        # show filtered not added user songs in pagination format
        pass
    elif album_id and song_id and request.method=='POST':
        # add song in album
        pass
    else:
        flash('Error while adding song into album','error')
        return redirect(url_for('creatorhome'))
#remove song from album
@app.route('/creator/albums/<int:album_id>/remove/<int:song_id>')
@allowed_for(['creator'])
@not_in_blacklist
def from_album_remove_song(album_id,song_id):
    album = Album.query.get(album_id); song = Song.query.get(song_id)
    if album.user_id != session['user_id']:
        flash('Not your album to add song!','warning')
        return redirect(url_for('creator_home'))
    if song in album.songs:
        album.songs.remove(song)
        flash('Removed song from album','success')
    else:
        flash('Song not in album to remove!','warning')
    return redirect(f'/creator/albums/{album_id}')

    
        



