from flask_wtf import Form
from wtforms.fields import StringField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class PostForm(Form):
    entry = StringField('Enter post content:')
    title = StringField('Enter post title:')