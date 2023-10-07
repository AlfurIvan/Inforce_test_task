from django.contrib.auth import models as auth_models
from django.db import models


class UserManager(auth_models.BaseUserManager):
    """Managers for creation user and superuser"""
    def create_user(self, first_name: str, last_name: str, email: str, password: str = None,
                    is_staff=False, is_superuser=False) -> "User":
        if not email:
            raise ValueError("User must have an email")
        elif not first_name:
            raise ValueError("User must have a first name")
        elif not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save()

        return user


class User(auth_models.AbstractUser):
    """User model, which uses by Employees and Restaurant(like single manager)"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Restaurant(models.Model):
    """Extension for 'single managers' to relate on restaurant, which offers menu"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="restaurant")
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, default='delivery')
    description = models.CharField(max_length=1023)
    info_href = models.CharField(max_length=255)
