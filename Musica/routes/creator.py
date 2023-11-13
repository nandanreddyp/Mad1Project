from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

from Musica.routes.permissions import *
from Musica.functions import save_file, remove_file


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
        return render_template('creator/upload.html')
    elif request.method == 'POST':
        data = request.form; files = request.files
        song = files['song']; cover = files.get('cover')
        title = data.get('title'); artist = data.get('artist'); 
        language = data.get('language'); genre = data.get('genre'); 
        lyrics = data.get('lyrics')
        from Musica.functions import mp3_duration_cal, save_file
        new_song = Song(user_id=current_user.id, title=title, duration=mp3_duration_cal(song), language=language, artist=artist, genre=genre)
        db.session.add(new_song); db.session.commit()
        filename = save_file('song',new_song.id, song); new_song.filename = filename; 
        if cover:
            filename = save_file('image/song',new_song.id, cover); new_song.cover = filename
        if lyrics:
            filename = save_file('lyrics',new_song.id,lyrics); new_song.lyrics = filename
        db.session.commit()
        flash('Song uploaded successfully','success')
        return redirect(url_for('upload'))

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
    if request.method == 'GET' and album_id:
        album = Album.query.get(album_id)
        if album and album.user_id == current_user.id:
            return render_template('creator/sub-temp/album.html',album=album)
        else: flash('Not your album','error')
    elif request.method == 'POST' and not(album_id):
        # return filtered results
        pass
    elif request.method == 'POST' and album_id:
        # save edited form
        pass
    else :
        # albums = db.select(Album).filter_by(user_id=current_user.id)
        albums = Album.query.filter_by(user_id=current_user.id).all()
        return render_template('creator/albums.html', albums=albums)
    return redirect(url_for('albums_creator'))

##Song routes##
##############################################################################################################################
#update & delete
@app.route('/creator/uploads/<int:song_id>/<way>',methods=['GET','POST'])
@not_in_blacklist
def upload_edit(song_id):
    song = Song.query.get(song_id)
    if way == 'update' and song:
        if request.method == 'GET':
            return render_template('creator/song_update.html',song=song)
        elif request.method == 'POST':
            # update song details
            pass
        pass
    elif way == 'delete' and song:
        if song_id and song:
            db.session.delete(song); db.session.commit()
            remove_file('image/profile',current_user.cover)
            # remove file in uploads also
            flash('Successfully deleted song','success')
        else:
            flash('Error deleting song!','error')
    return redirect('/uploads')
#assign a song to a particular album
@app.route('/creator/uploads/<int:song_id>/<way>/albums/<int:album_id>')
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
        return render_template('creator/sub-temp/album-create.html')
    elif request.method == 'POST':
        data = request.form; cover = request.files.get('cover')
        title = data.get('title'); artist = data.get('artist')
        album = Album(title=title, artist=artist, user_id=current_user.id)
        db.session.add(album)
        if cover:
            from Musica.functions import save_file
            cover = save_file('image/album',album.id,cover); album.cover = cover
        db.session.commit()
        flash('Created album','success')
        return redirect(url_for('albums_creator'))
#update
@app.route('/creator/albums/<int:album_id>/<way>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def album_edit(album_id,way):
    album = Album.query.get(album_id)
    if way == 'update':
        if request.method == 'GET' and album:
            return render_template('creator/sub-temp/album-update.html',album=album)
        elif request.method == 'POST' and album:
            data = request.form; file = request.files.get('cover')
            album.title = data['title']; album.artist = data['artist']; delete = data.get('cover-delete')
            if file and not(delete):
                image_loc = save_file('image/album',current_user.id,file)
                album.cover = image_loc
            elif album.cover and delete:
                remove_file('image/album',album.cover)
                album.cover = None
            db.session.commit()
            flash('Updated album details!','success')
        else: flash('Error occured!','error')
        return redirect(f'/creator/albums/{album_id}')
    elif way == 'delete':
        if album:
            if album.cover: remove_file('image/album',album.cover)
            db.session.delete(album); db.session.commit()
            flash('Successfully deleted album','success')
            return redirect('/creator/albums')
        else:
            flash('Error deleting album!','error')
            return redirect('creator/albums')
            
#assign a album a particular song
@app.route('/creator/albums/<int:album_id>/<way>/songs/',defaults={'song_id':None})
@app.route('/creator/albums/<int:album_id>/<way>/songs/<int:song_id>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def from_album_add_song(album_id,song_id,way):
    print(request.url_rule.endpoint)
    album = Album.query.get(album_id); song = Song.query.get(song_id)
    if album and not(song) and request.method=='GET':
        # show not added user songs in pagination format
        songs = Song.query.filter_by(user_id=current_user.id).all()
        return render_template('creator/sub-temp/album~add-rem.html',songs=songs,album=album)
    elif album and not(song) and request.method=='POST':
        # show filtered not added user songs in pagination format
        return render_template('creator/sub-temp/album~add-rem.html',songs=songs,album=album)
    elif album and song and request.method=='POST' and way=='add':
        if song.user.id == current_user.id and song not in album.songs:
            album.songs.append(song); db.session.commit()
            flash('Song added into album','success')
        else:
            flash('Song already in album','error')
    elif album and song and request.method=='POST' and way=='remove':
        if song in album.songs:
            album.songs.remove(song); db.session.commit()
            flash('Song removed from album','success')
        else:
            flash('Song not in album','error')
    else:
        flash('Error occured!','error')
    return redirect(f'/creator/albums/{album_id}')

