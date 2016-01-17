from datetime import datetime

from sqlalchemy import desc

from Flask_Blog import db


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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    postedEntries = db.relationship('BlogEntry', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username