from Musica import app
from Musica.database.models import *
from flask import session, render_template, flash, redirect, url_for, request

from Musica.routes.permissions import *
from Musica.functions import save_file, remove_file, get_lyrics


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
def creator_home():
    session['currentPage']='creator_home'
    recent = Song.query.filter_by(user_id=current_user.id).order_by(Song.time_added.desc()).first()
    viewed = Song.query.filter_by(user_id=current_user.id).order_by(Song.play_count.desc()).first()
    positive = Song.query.filter_by(user_id=current_user.id).order_by(Song.rating.desc()).first()
    negative = Song.query.filter_by(user_id=current_user.id).order_by(Song.rating.asc()).first()
    return render_template('creator/home.html',recent=recent,viewed=viewed,positive=positive,negative=negative)
    
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
    song = Song.query.get(song_id)
    if request.method == 'GET' and song:
        if song.user_id == current_user.id:
            if song.lyrics:
                lyrics = get_lyrics(song.lyrics)
            else:
                lyrics = None
            return render_template('creator/sub-temp/song.html',song=song,lyrics=lyrics)
        flash('You are not owner of that song!','warning')
        return redirect(url_for('all_uploads'))
    elif request.method == 'GET' and not(song):
        view = request.args.get('view',6,type=int)
        songs = Song.query.filter_by(user_id=current_user.id).order_by(Song.time_added.desc()).paginate(page=1, per_page=view) 
        return render_template('creator/uploads.html',songs=songs,view=view+6)
    elif request.method == 'POST' and not(song):
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
            elif sort_by == 'alphabetical': filtered = filtered.order_by(func.lower(Song.title).asc())
        filtered = filtered.paginate(page=1,per_page=view)
        flash('Filter applied','success')
        return render_template('creator/uploads.html',songs=filtered,view=view+6,filter=True)

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
    elif request.method == 'GET' and not(album_id):
        albums = Album.query.filter_by(user_id=current_user.id).order_by(Album.time_added.desc()).all()
        return render_template('creator/albums.html', albums=albums)
    elif request.method == 'POST' and not(album_id) :
        data = request.form; album_name = data.get('album'); artist_name = data.get('artist'); sort_by = data.get('sortby')
        filtered = Album.query.filter_by(user_id=current_user.id)
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
        return render_template('creator/albums.html',albums=filtered,filter=True)
    return redirect(url_for('albums_creator'))

##Song routes##
##############################################################################################################################
#update & delete
@app.route('/creator/uploads/<int:song_id>/<way>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def upload_edit(song_id,way):
    song = Song.query.get(song_id)
    if way == 'update' and song:
        if request.method == 'GET':
            if song.lyrics: lyrics = get_lyrics(song.lyrics)
            else: lyrics = None
            return render_template('creator/sub-temp/song-update.html',song=song,lyrics=lyrics)
        elif request.method == 'POST':
            data = request.form; files = request.files; song_file = files['song']; cover = files.get('cover'); lyrics = data.get('lyrics')
            song.title = data.get('title')
            song.artist = data.get('artist')
            song.language = data.get('language')
            song.genre = data.get('genre')
            from Musica.functions import mp3_duration_cal, save_file, remove_file
            if song_file:
                remove_file('song',song.filename)
                song.duration = mp3_duration_cal(song_file)
                filename = save_file('song',song.id, song_file)
                song.filename = filename
            if cover:
                if song.cover: remove_file('image/song',song.cover)
                filename = save_file('image/song',song.id, cover)
                song.cover = filename
            if lyrics:
                filename = save_file('lyrics',song.id,lyrics)
                song.lyrics = filename
            db.session.commit()
            flash('Song updated successfully','success')
        return redirect(f'/creator/uploads/{song_id}')
    elif way == 'delete' and song:
        if song and song.user_id == current_user.id:
            from Musica.functions import mp3_duration_cal, save_file, remove_file
            if song.cover: remove_file('image/song',song.cover)
            if song.lyrics: remove_file('lyrics',song.lyrics)
            remove_file('song',song.filename)
            db.session.delete(song); db.session.commit()
            flash('Successfully deleted song','success')
        else:
            flash('Error deleting song!','error')
    return redirect('/creator/uploads')

#assign a song to a particular album
@app.route('/creator/uploads/<int:song_id>/<way>/albums/',defaults={'album_id':None}, methods=['GET','POST'])
@app.route('/creator/uploads/<int:song_id>/<way>/albums/<int:album_id>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def from_song_add_album(song_id,album_id,way):
    session['currentPage']='uploads'
    song = Song.query.get(song_id); album = Album.query.get(album_id)
    if song and not(album) and request.method=='GET':
        albums = Album.query.filter_by(user_id=current_user.id).order_by(Album.time_added.desc()).all()
        return render_template('creator/sub-temp/song~add-rem.html',song=song,albums=albums)
    elif song and not(album) and request.method=='POST':
        data = request.form; album_name = data.get('album'); artist_name = data.get('artist'); sort_by = data.get('sortby')
        filtered = Album.query.filter_by(user_id=current_user.id)
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
        return render_template('creator/sub-temp/song~add-rem.html',song=song,albums=filtered,filter=True)
    elif song and album and request.method=='POST':
        if way == 'add':
            album.songs.append(song)
            db.session.commit()
            flash('Song added into album','success')
        elif way == 'remove':
            album.songs.remove(song)
            db.session.commit()
            flash('Song removed from album','success')
        return redirect(f'/creator/uploads/{song_id}/add/albums')
    else:
        flash('Error while adding/removing song from album','error')
        return redirect(url_for('creator_home'))


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
        db.session.add(album); db.session.commit()
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
@app.route('/creator/albums/<int:album_id>/<way>/songs/',defaults={'song_id':None},methods=['GET','POST'])
@app.route('/creator/albums/<int:album_id>/<way>/songs/<int:song_id>',methods=['GET','POST'])
@allowed_for(['creator'])
@not_in_blacklist
def from_album_add_song(album_id,song_id,way):
    session['currentPage']='albums'
    print(request.url_rule.endpoint)
    album = Album.query.get(album_id); song = Song.query.get(song_id)
    if album and not(song) and request.method=='GET':
        view = request.args.get('view',6,type=int)
        songs = Song.query.filter_by(user_id=current_user.id).order_by(Song.time_added.desc()).paginate(page=1, per_page=view) 
        return render_template('creator/sub-temp/album~add-rem.html',songs=songs,album=album,view=view+6)
    elif album and not(song) and request.method=='POST':
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
        return render_template('creator/sub-temp/album~add-rem.html',songs=filtered,album=album,filter=True,view=view+6)
    elif album and song and request.method=='POST' and way=='add':
        if song.user.id == current_user.id and song not in album.songs:
            album.songs.append(song); db.session.commit()
            flash('Song added into album','success')
            return redirect(f'/creator/albums/{album_id}/add/songs')
        else:
            flash('Song already in album','error')
    elif album and song and request.method=='POST' and way=='remove':
        fromm = request.args.get('from',None)
        print(fromm)
        if song in album.songs:
            album.songs.remove(song); db.session.commit()
            flash('Song removed from album','success')
            if not(fromm): return redirect(f'/creator/albums/{album_id}')
            else: return redirect(f'/creator/albums/{album_id}/add/songs')
        else:
            flash('Song not in album','error')
    else:
        flash('Error occured!','error')
    return redirect(f'/creator/albums/{album_id}')

