# https://flask-login.readthedocs.io/en/latest/
# pip install flask-login

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

path = os.path.abspath(os.getcwd()) + '\\app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + path

db = SQLAlchemy(app)
db.create_all(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    contact = db.Column(db.String(200))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    # when button to sign up on login page is clicked
    if request.method == 'GET':
        return render_template('sign_up.html')

    elif request.method == 'POST':
        # return redirect(url_for('index'))

        # check that email is not already registered
        user = db.session.query(User).filter(User.email==request.form['email']).first()
        if not user:
            user = User(email=request.form['email'],password=request.form['password'],contact=request.form['contact'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('This email already has an account.')
            # makes more sense to redirect a registered user to login page
            return render_template('login.html')
            # return render_template('sign_up.html')

# route will depend on whether how we structure pages
# is index the login + homepage or the page selecting preferences to then be matched?
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        #return redirect(url_for('index'))
        user = db.session.query(User).filter(User.email==request.form['email'], password=request.form['password']).first()
        # check that the user is in the database
        if not user:
            flash('This email does not have an account.')
        login_user(user)
        return redirect(url_for('index'))

# placeholder reference to homepage
@app.route('/', methods=['GET','POST'])
# @login_required
def index():
    ## take login as the default index pages
    return render_template('index.html')

@app.route('/logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for(('login'))

if __name__ == '__main__':
    sess.init_app(app)
    app.run(debug=True)
