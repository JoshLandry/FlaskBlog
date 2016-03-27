import os
import Flask_Blog
import unittest
import tempfile

class Flask_BlogTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, Flask_Blog.app.config['DATABASE'] = tempfile.mkstemp()
        Flask_Blog.app.config['TESTING'] = True
        self.app = Flask_Blog.app.test_client()
        Flask_Blog.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(Flask_Blog.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()