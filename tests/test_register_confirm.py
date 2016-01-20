import unittest
from app.models import User


class UserRegisterConfirmTestCase(unittest.TestCase):
    def test_generate_token(self):
        u = User(id=100)
        token = u.generate_confirmation_token()
        print token
        self.assertTrue(token is not None)

    def test_confirm(self):
        u = User(id=100)
        token = u.generate_confirmation_token()
        t = u.confirm(token)
        self.assertTrue(t)
