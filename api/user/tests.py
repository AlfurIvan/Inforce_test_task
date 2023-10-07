import datetime
from django.test import TestCase
from django.conf import settings
import jwt
from .services import create_token, create_user, user_email_selector, UserDataClass
from .models import User, Restaurant


class CreateTokenTestCase(TestCase):
    def test_create_token(self):
        user_id = 1
        settings.JWT_SECRET = 'your_jwt_secret'  # Підставте свій секрет

        # Викликаємо метод create_token
        token = create_token(user_id)

        # Перевірка, що токен є рядком
        self.assertIsInstance(token, str)

        # Розшифровуємо токен
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        # Перевірка, що токен містить правильний ID користувача
        self.assertEqual(decoded_token.get("id"), user_id)

        # Перевірка, що токен є дійсним
        self.assertTrue(decoded_token)

        # Перевірка, що токен дійсний протягом 24 годин
        expiration_time = datetime.datetime.utcfromtimestamp(decoded_token["exp"])
        current_time = datetime.datetime.utcnow()
        self.assertTrue(expiration_time > current_time)
        self.assertTrue(expiration_time - current_time <= datetime.timedelta(hours=24))


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        # Створимо тестовий об'єкт UserDataClass
        user_dc = UserDataClass(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
           company="some",
        )

        # Викликаємо метод create_user
        created_user_dc = create_user(user_dc)

        # Перевірка, що метод повертає правильний тип об'єкта
        self.assertIsInstance(created_user_dc, UserDataClass)

        # Перевірка, що об'єкт був створений в базі даних
        user_in_db = User.objects.get(email=user_dc.email)
        self.assertEqual(user_in_db.first_name, user_dc.first_name)
        self.assertEqual(user_in_db.last_name, user_dc.last_name)
        self.assertEqual(user_in_db.email, user_dc.email)
        # Перевірка паролю, важлива тільки якщо він був наданий
        if user_dc.password:
            self.assertTrue(user_in_db.check_password(user_dc.password))


class UserEmailSelectorTestCase(TestCase):
    def setUp(self):
        # Створимо тестового користувача для бази даних
        self.test_user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )

    def test_user_email_selector(self):
        # Викликаємо метод user_email_selector
        found_user = user_email_selector("john@example.com")

        # Перевірка, що метод повертає правильний тип об'єкта
        self.assertIsInstance(found_user, User)

        # Перевірка, що метод знайшов правильного користувача
        self.assertEqual(found_user, self.test_user)

    def test_user_email_selector_not_found(self):
        # Викликаємо метод user_email_selector для невірної email
        not_found_user = user_email_selector("nonexistent@example.com")

        # Перевірка, що метод повертає None, коли користувача не знайдено
        self.assertIsNone(not_found_user)