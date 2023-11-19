from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

# for time song and palylist added:
from datetime import datetime

db = SQLAlchemy()

# models
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String,primary_key=True); password = db.Column(db.String,nullable=False)
    f_name = db.Column(db.String,nullable=False); l_name = db.Column(db.String)
    premium = db.Column(db.Boolean,default=False); cover = db.Column(db.String)
    role = db.Column(db.String,default='user'); library = db.relationship('Library',backref='user',uselist=False)

    played = db.relationship('Play',back_populates='user',cascade='all, delete-orphan')
    playlists = db.relationship('Playlist',back_populates='user',cascade="all, delete-orphan")
    songs = db.relationship('Song',back_populates='user',cascade="all, delete-orphan")
    albums = db.relationship('Album',back_populates='user',cascade="all, delete-orphan")
    ratings = db.relationship('Rating',back_populates='user',cascade="all, delete-orphan")
    library = db.relationship('Library',back_populates='user',uselist=False,cascade='all, delete-orphan')
    blacklist = db.relationship('Blacklist',back_populates='user',uselist=False,cascade='all, delete-orphan')

# many to many relationships declaration
album_song_association = db.Table('album_song_association',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)
playlist_song_association = db.Table('playlist_song_association',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)    
library_song_association = db.Table('library_song_association',
    db.Column('library_id',db.String,db.ForeignKey('library.user_id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'))
)
library_album_association = db.Table('library_album_association',
    db.Column('library_id',db.String,db.ForeignKey('library.user_id')),
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'))
)
library_playlist_association = db.Table('library_playlist_associatin',
    db.Column('library_id',db.String,db.ForeignKey('library.user_id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'))
)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); filename = db.Column(db.String); 
    title = db.Column(db.String,nullable=False); duration = db.Column(db.String,nullable=False)
    time_added = db.Column(db.DateTime, default=datetime.utcnow); 
    lyrics = db.Column(db.String); 
    cover = db.Column(db.String); 
    language = db.Column(db.String,nullable=False)
    artist = db.Column(db.String)
    genre = db.Column(db.String)
    flagged = db.Column(db.Boolean,default=False)
    # analytics useage
    play_count = db.Column(db.Integer, default=0)
    plays = db.relationship('Play',back_populates='song',cascade='all, delete-orphan')
    rating = db.Column(db.Float, default=0.0)
    ratings = db.relationship('Rating',back_populates='song',cascade="all, delete-orphan")
    #
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='songs')

    albums = db.relationship('Album', secondary=album_song_association, single_parent=True, back_populates='songs', lazy=True)
    playlists = db.relationship('Playlist', secondary=playlist_song_association, single_parent=True, back_populates='songs', lazy=True)
    library = db.relationship('Library',secondary=library_song_association, single_parent=True, back_populates='songs', lazy=True)

class Rating(db.Model):
    __tablename__ = 'Song_ratings'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='ratings')

    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    song = db.relationship('Song',back_populates='ratings')

class Play(db.Model):
    __tablename__ = 'Song_plays'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='played')

    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    song = db.relationship('Song',back_populates='plays')

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable=False); artist = db.Column(db.String); cover = db.Column(db.String)
    time_added = db.Column(db.DateTime, default=datetime.utcnow)
    flagged = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='albums')

    songs = db.relationship('Song', secondary=album_song_association, back_populates='albums', lazy=True)
    libraries = db.relationship('Library',secondary=library_album_association, single_parent=True, back_populates='albums', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); title = db.Column(db.String,nullable=False)
    time_added = db.Column(db.DateTime, default=datetime.utcnow); public = db.Column(db.Boolean,default=False)

    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='playlists')

    songs = db.relationship('Song', secondary=playlist_song_association, back_populates='playlists', lazy=True)
    libraries = db.relationship('Library',secondary=library_playlist_association, single_parent=True, back_populates='playlists', lazy=True)

class Library(db.Model):
    __tablename__ = 'library'
    user_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User',back_populates='library')

    songs = db.relationship('Song', secondary=library_song_association, lazy=True)
    albums = db.relationship('Album', secondary=library_album_association, lazy=True)
    playlists = db.relationship('Playlist', secondary=library_playlist_association, lazy=True)

# admin required
class Blacklist(db.Model):
    __tablename__ = 'blaklist'
    id = db.Column(db.Integer,primary_key=True)
    time_added = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.String, db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='blacklist')

class PremiumReq(db.Model):
    __tablename__ = 'premium_requests'
    id = db.Column(db.Integer,primary_key=True)
    time_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    trans_id = db.Column(db.String)
