import os
import Flask_Blog
from Flask_Blog import app, User, BlogEntry, Tag
import unittest
from flask_sqlalchemy import SQLAlchemy
import tempfile

class Flask_BlogTestCase(unittest.TestCase):

    def setUp(self):
        Flask_Blog.db.drop_all()
        Flask_Blog.db.create_all()
        print 'Created test DB.'

    def tearDown(self):
        Flask_Blog.db.drop_all()

    def test_add_user(self):
        TestUser = User(username="testuser", email="test@yahoo.com", password="yokel")
        Flask_Blog.db.session.add(TestUser)
        Flask_Blog.db.session.commit()
        print 'Added test user.'

    def test_add_post(self):
        TestUser = User(username="testuser", email="test@yahoo.com", password="yokel")
        def add_post(artist, title, entry, rating, tags):
            Flask_Blog.db.session.add(BlogEntry(artist=artist, title=title, entry=entry, rating=rating, user=TestUser, tags=tags))

        for name in ["ambient", "noise", "avant garde"]:
            Flask_Blog.db.session.add(Tag(name=name))
        Flask_Blog.db.session.commit()

        add_post("The Twentieth Century", "The Twentieth Century", "review", "4", "ambient,noise")
        Flask_Blog.db.session.commit()
        print 'Added test post.'

if __name__ == '__main__':
    unittest.main()