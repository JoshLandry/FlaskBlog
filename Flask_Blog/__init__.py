import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

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
from werkzeug.security import check_password_hash, generate_password_hash

tags = db.Table('entry_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('blog_entry.id'))
)

class BlogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    entry = db.Column(db.String(300))
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags,
                            backref=db.backref('entries', lazy='dynamic'))

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
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.name

#

# from forms import PostForm, LoginForm, SignupForm

#

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo,\
    url, ValidationError

class PostForm(Form):
    entry = StringField('Enter your review of the album:')
    artist = StringField('Enter the artist that created this album:')
    title = StringField('Enter the album title:')
    rating = IntegerField('Rate the album out of 5:')

class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class SignupForm(Form):
    username = StringField('Username',
                    validators=[
                        DataRequired(), Length(3, 80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Usernames consist of numbers, letters,'
                                    'and underscores.')])
    password = PasswordField('Password',
                    validators=[
                        DataRequired(),
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                    validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
          raise ValidationError('This username is already taken.')

#

# import views

#

from flask import render_template, url_for, redirect, flash, abort
from flask_login import login_required, login_user, logout_user, current_user

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
        artist = form.artist.data
        entry = form.entry.data
        title = form.title.data
        rating = form.rating.data
        newEntry = BlogEntry(user=current_user, title=title, entry=entry, rating=rating, artist=artist)
        db.session.add(newEntry)
        db.session.commit()
        flash("Stored entry: '{}'".format(title))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = BlogEntry.query.get_or_404(entry_id)
    if current_user != entry.user:
        abort(403)
    form = PostForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash("Stored '{}'".format(entry.title))
        return redirect(url_for('user', username=current_user.username))
    return render_template('ReviewForm.html', form=form, title="Edit entry")


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(url_for('user', username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500