import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '.t\xe5\xc37\xf6\xa9(\x81\xbe\x89#\xee\x00\xdf\x87\xfab\xd5\xe7FQ:%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Flask_Blog.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# configure auth
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# import models

from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin

class BlogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    entry = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        return BlogEntry.query.order_by(desc(BlogEntry.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.entry, self.title)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    postedEntries = db.relationship('BlogEntry', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

# import views

from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user

from forms import PostForm, LoginForm

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_posts=BlogEntry.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostForm()
    if form.validate_on_submit():
        entry = form.entry.data
        title = form.title.data
        newEntry = BlogEntry(user=logged_in_user(), title=title, entry=entry)
        db.session.add(newEntry)
        db.session.commit()
        flash("Stored entry: '{}'".format(title))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(url_for('index'))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500