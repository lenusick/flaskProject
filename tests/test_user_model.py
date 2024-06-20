import unittest
from app.models import User, Role, Permission
from app import create_app


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User()
        user.set_password("hash")
        self.assertTrue(user.password_hash is not None)

    def test_password_no_getter(self):
        user = User()
        user.set_password("hash")
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verify(self):
        user = User()
        user.set_password("hash")
        self.assertTrue(user.password_verify("hash"))
        self.assertFalse(user.password_verify("test"))

    def test_salt(self):
        user = User()
        user.set_password("hash")
        user2 = User()
        user2.set_password("hash")
        self.assertTrue(user.password_hash != user2.password_hash)

    def test_user_role(self):
        Role.insert_roles()
        user = User(email='lminlisa@gmail.com')
        user.set_password("123")
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))
