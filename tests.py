import unittest
from app import app, db
from app.models import WebUser


class WebUserModelCase(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://<dbUser>:<dbPassword>@<host>/<dbName>"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = WebUser(username="susan")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))

    def test_avatar(self):
        u = WebUser(username="john", email="john@example.com")
        self.assertEqual(u.avatar(128), ("https://www.gravatar.com/avatar/"
                                         "d4c74594d841139328695756648b6bd6"
                                         "?d=identicon&s=128"))
if __name__ == "__main__":
    unittest.main(verbosity=2)