import os
cwd = os.getcwd()

# creating flask instance
from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret key lady gaga'

# database connectivity
database_path = os.path.join(cwd,'Musica','database','database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
from .database.models import db
db.init_app(app)
# migrate database
from flask_migrate import Migrate
migrate_path = os.path.join(cwd,'Musica','database','migrate')
migrate = Migrate(app, db, directory=migrate_path)

# api connectivity
from .resources import api
api.init_app(app)

# creating api endpoints
from .routes import welcome
from .routes import permissions
from .routes import user
from .routes import creator
from .routes import admin

# Create a Flask app instance without running it
app.app_context().push()
