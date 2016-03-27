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

if __name__ == '__main__':
    unittest.main()