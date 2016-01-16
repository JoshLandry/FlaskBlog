from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, flash

from forms import PostForm

app = Flask(__name__)

posts = []
app.config['SECRET_KEY'] = '.t\xe5\xc37\xf6\xa9(\x81\xbe\x89#\xee\x00\xdf\x87\xfab\xd5\xe7FQ:%'
def save_post(entry, title):
  posts.append(dict(
        entry = entry,
        title = title,
        user = "landry",
        date = datetime.utcnow()
    ))

def new_posts(num):
  return sorted(posts, key=lambda bm: bm['date'], reverse=True) [:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_posts=new_posts(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PostForm()
    if form.validate_on_submit():
        entry = form.entry.data
        title = form.title.data
        save_post(entry, title)
        flash("Stored entry: '{}'".format(title))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)