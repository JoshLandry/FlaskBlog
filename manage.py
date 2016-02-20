#! /usr/bin/env python

from Flask_Blog import app, db, User, BlogEntry, Tag
from flask.ext.script import Server, Manager, prompt_bool
# from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())

@manager.command
def initdb():
    db.create_all()

    BoyLandry = User(username="BoyLandry", email="bluemazaro@yahoo.com", password="yokel")

    db.session.add(BoyLandry)
    db.session.add(User(username="Goatness", email="goat@goatcontrol.usa", password="goethe"))
    db.session.commit()
    print 'Initialized the database'

    def add_post(artist, title, entry, rating, tags):
        db.session.add(BlogEntry(artist=artist, title=title, entry=entry, rating=rating, user=BoyLandry, tags=tags))

    for name in ["ambient", "noise", "avant garde"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_post("The Twentieth Century", "The Twentieth Century", "review", "4", "ambient,noise")

    db.session.commit()

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()