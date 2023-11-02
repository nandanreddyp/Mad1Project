from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

# many-to-many relationship

playlist_song_association = db.Table('playlist_song_association',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)
album_song_association = db.Table('album_song_association',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)


# models

from flask_login import UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.String,primary_key=True); password = db.Column(db.String,nullable=False)
    f_name = db.Column(db.String,nullable=False); l_name = db.Column(db.String)
    premium = db.Column(db.Boolean,default=False); role = db.Column(db.String,default='user')
    # one-to-many relationship with songs
    songs = db.relationship('Song', backref='uploader', lazy=True, cascade="all, delete-orphan")
    # one-to-many relationship with albums
    albums = db.relationship('Album', backref='creator',lazy=True,cascade='all, delete-orphan')
    # one-to-many relationship with playlists
    playlists = db.relationship('Playlist',backref='creator',lazy=True,cascade="all, delete-orphan")

class Song(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); title = db.Column(db.String,nullable=False); duration = db.Column(db.String,nullable=False)
    upload_time = db.Column(db.Time,default=func.current_time()); artist = db.Column(db.String); lyrics = db.Column(db.Boolean)
    # foreign key relationship to user
    uploader = db.Column(db.String, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    # Define the many-to-many relationship with playlists and enable cascade
    albums = db.relationship('Album', secondary=album_song_association, back_populates='songs',lazy=True,cascade='all, delete-orphan')
    # Define the many-to-many relationship with playlists and enable cascade
    playlists = db.relationship('Playlist', secondary=playlist_song_association, back_populates='songs', cascade="all, delete-orphan")

class Album(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String,nullable=False); artist = db.Column(db.String); cover = db.Column(db.Boolean)
    # foreign key relationship to user
    creator = db.Column(db.String, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    # many-to-many relationship with songs and enable cascade
    songs = db.relationship('Song', secondary=album_song_association, back_populates='albums', cascade='all, delete-orphan', lazy=True)
    

class Playlist(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True); title = db.Column(db.String,nullable=False)
    # foreign key relationship to User
    creator = db.Column(db.String, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    # Define the many-to-many relationship with songs and enable cascade
    songs = db.relationship('Song', secondary=playlist_song_association, back_populates='playlists', cascade="all, delete-orphan", lazy=True)



 