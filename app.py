import os
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
current_dir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(current_dir, 'database.sqlite3')
#upload setting
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create the extension

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String)

# with app.app_context():
#     db.create_all()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add_file', methods=['POST','GET'])
def edit_file():
    if request.method=="GET":
        return render_template('add.html')
    elif request.method=='POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully: ' + filename
        else:
            return 'No file uploaded'
    elif request.method=='PUT':
        return render_template('update.html')
@app.route('/play',methods=['GET'])
def play_song():
    songs_paths=[]
    for song in os.listdir('uploads'):
        #songs_paths.append(os.path.join(app.config['UPLOAD_FOLDER'],song))
        songs_paths.append(song)
    return render_template('play.html',paths=songs_paths)

@app.route('/play/<filename>')
def play_music(filename):
    print(os.path.join('uploads',filename))
    return send_file(os.path.join('uploads', filename))

if __name__=='__main__':
    db.init_app(app)
    app.run()