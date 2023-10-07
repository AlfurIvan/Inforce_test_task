"""User services tests"""
import datetime
from django.test import TestCase
from django.conf import settings
import jwt
from .services import create_token, create_user, user_email_selector, UserDataClass
from .models import User


class CreateTokenTestCase(TestCase):
    def test_create_token(self):
        """Test for JWT token creation"""
        user_id = 1
        token = create_token(user_id)
        self.assertIsInstance(token, str)

        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        self.assertTrue(decoded_token)
        self.assertEqual(decoded_token.get("id"), user_id)

        expiration_time = datetime.datetime.utcfromtimestamp(decoded_token["exp"])
        current_time = datetime.datetime.utcnow()
        self.assertTrue(expiration_time > current_time)
        self.assertTrue(expiration_time - current_time <= datetime.timedelta(hours=24))


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        """Test for creating new user from dataclass"""
        user_dc = UserDataClass(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            company="some",
        )

        created_user_dc = create_user(user_dc)
        self.assertIsInstance(created_user_dc, UserDataClass)

        user_in_db = User.objects.get(email=user_dc.email)
        self.assertEqual(user_in_db.first_name, user_dc.first_name)
        self.assertEqual(user_in_db.last_name, user_dc.last_name)
        self.assertEqual(user_in_db.email, user_dc.email)
        if user_dc.password:
            self.assertTrue(user_in_db.check_password(user_dc.password))


class UserEmailSelectorTestCase(TestCase):
    """tests for fetching user by email method"""

    def setUp(self):
        self.test_user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )

    def test_user_email_selector(self):
        found_user = user_email_selector("john@example.com")
        self.assertIsInstance(found_user, User)
        self.assertEqual(found_user, self.test_user)

    def test_user_email_selector_not_found(self):
        not_found_user = user_email_selector("nonexistent@example.com")
        self.assertIsNone(not_found_user)
