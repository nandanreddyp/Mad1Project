from Musica import app
from Musica.database.models import *
from flask import session, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user



# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from .permissions import *

@app.route('/')
def home():
    return render_template('user/dashboard.html')

@app.route('/in',methods=['GET','POST'])
def welcome():
    if request.method == 'POST':
        session['id'] = request.form['email']
        exists = User.query.get(session['id'])
        if exists:
            return redirect(url_for('login'))
        return redirect(url_for('signup'))
    return render_template('welcome/welcome.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        session['id']=data['email']
        if User.query.get(session['id']):
            flash('User already exists','info')
            return redirect(url_for('login'))
        from Musica.functions import hash
        user = User(id=data['email'],password=hash(data['password']),f_name=data['f_name'],l_name=data['l_name'])
        db.session.add(user); db.session.commit()
        flash('Account created successfully','success')
        flash('Login to your account','info')
        return redirect(url_for('login'))
    return render_template('welcome/signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        user = User.query.get(session['id'])
        from Musica.functions import password_check
        if user and password_check(user.password, data['password']):
            flash('Correct password entered!','success')
            login_user(user)
            return redirect(url_for('home'))
        flash('Wrong password entered!','warning')
        return redirect(url_for('login'))
    elif session.get('id'):
        session['name']=User.query.get(session['id']).f_name
        return render_template('welcome/login.html')
    return redirect(url_for('welcome'))

@app.route('/logout',methods=['GET'])
def logout():
    logout_user();session.clear()
    flash('You have been logged out successfully','success')
    return redirect(url_for('welcome'))