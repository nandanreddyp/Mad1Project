from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

import os
current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir, 'database.sqlite3')
db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    user_id = db.Column(db.String,primary_key=True)
    password = db.Column(db.String,unique=True)
    premium = db.Column(db.String,unique=True)
    
# class Song(db.Model):
#     __tablename__ = 'Song details'
#     song_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     file_link = db.Column(db.String,nullable=False)
#     lyrics = db.Column(db.String)
#     name = db.Column(db.String(100),nullable=False)
#     genre = db.Column(db.String(100))
#     artist = db.Column(db.String(100))
#     # student_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     # roll_number=db.Column(db.String(100), nullable=False, unique=True)
#     # first_name=db.Column(db.String(100), nullable=False)
#     # last_name=db.Column(db.String(100))
# class Playlist(db.Model):
#     __tablename__ = 'Playlist details'
#     plylist_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     # courses = {'course_1':1, 'course_2':2, 'course_3':3, 'course_4':4}
#     # course_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     # course_code=db.Column(db.String(100), nullable=False, unique=True)
#     # course_name=db.Column(db.String(100), nullable=False)
#     # course_description=db.Column(db.String(100))
# class Album(db.Model):
#     __tablename__ = 'Album details'
#     album_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     # enrollment_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     # estudent_id=db.Column(db.Integer, db.ForeignKey('student.student_id'),nullable=False)
#     # ecourse_id=db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

## run once to create database
#db.create_all()

# for x in ['nandano','sukanya','nandan12']:
#     nandan = User(user_id='x')
#     db.session.add(nandan)
#     db.session.commit()

print(User.query.all())
