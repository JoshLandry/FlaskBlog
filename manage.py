#! /usr/bin/env python

from Flask_Blog import app, db, User
# from Flask_Blog.models import User
from flask.ext.script import Server, Manager, prompt_bool

server = Server(port=9000)

manager = Manager(app)
manager.add_command("runserver", Server())

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="landry", email="bluemazaro@yahoo.com", password="test"))
    db.session.add(User(username="goatness", email="goat@goatcontrol.usa", password="test"))
    db.session.commit()
    print 'Initialized the database'

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()