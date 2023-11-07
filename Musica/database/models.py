from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
    # one-to-many relationship with songs
    songs = db.relationship('Song', backref='uploader', lazy=True, cascade="all, delete-orphan")
    # one-to-many relationship with albums
    albums = db.relationship('Album', backref='creator',lazy=True,cascade='all, delete-orphan')
    # one-to-many relationship with playlists
    playlists = db.relationship('Playlist',backref='creator',lazy=True,cascade="all, delete-orphan")
    # one to many relationship with ratings
    ratings = db.relationship('Rating',back_populates='user',cascade="all, delete-orphan")

# many to many relationship declaration
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
library_palylist_association = db.Table('library_playlist_associatin',
    db.Column('library_id',db.String,db.ForeignKey('library.user_id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'))
)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); title = db.Column(db.String,nullable=False); duration = db.Column(db.String,nullable=False)
    time_added = db.Column(db.DateTime, default=datetime.utcnow); artist = db.Column(db.String); 
    lyrics = db.Column(db.String); cover = db.Column(db.String); 
    # analytics useage
    play_count = db.Column(db.Integer, default=0)
    ratings = db.relationship('Rating',back_populates='song',cascade="all, delete-orphan")
    # foreign key relationship to user
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    # Define the many-to-many relationship with playlists and enable cascade
    albums = db.relationship('Album', secondary=album_song_association, single_parent=True, back_populates='songs', lazy=True)
    # Define the many-to-many relationship with albums and enable cascade
    playlists = db.relationship('Playlist', secondary=playlist_song_association, single_parent=True, back_populates='songs', lazy=True)
    # Define the many-to-one relationship with library 
    library = db.relationship('Library',secondary=library_song_association, single_parent=True, back_populates='songs', lazy=True)

class Rating(db.Model):
    __tablename__ = 'Song_ratings'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',back_populates='ratings')
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    song = db.relationship('Song',back_populates='ratings')
    rating = db.Column(db.Boolean, nullable=False)

class Blacklist(db.Model):
    __tablename__ = 'blaklist'
    creator_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable=False); artist = db.Column(db.String); cover = db.Column(db.Boolean)
    # foreign key relationship to user
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    # many-to-many relationship with songs and enable cascade
    songs = db.relationship('Song', secondary=album_song_association, back_populates='albums', lazy=True)

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); title = db.Column(db.String,nullable=False)
    # foreign key relationship to User
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    # Define the many-to-many relationship with songs and enable cascade
    songs = db.relationship('Song', secondary=playlist_song_association, back_populates='playlists', lazy=True)

class Library(db.Model):
    __tablename__ = 'library'
    user_id = db.Column(db.String, db.ForeignKey('users.id'), primary_key=True)
    # many-to-many relationship with songs
    songs = db.relationship('Song', secondary=library_song_association, lazy=True)
    # many-to-many relationship with albums
    albums = db.relationship('Album', secondary=library_album_association, lazy=True)
    # many-to-many relationship with playlists
    playlists = db.relationship('Playlist', secondary=library_palylist_association, lazy=True)



