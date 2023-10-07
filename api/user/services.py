"""Module with functionality"""
import dataclasses
import datetime
from typing import TYPE_CHECKING

import jwt
from django.conf import settings

from . import models

if TYPE_CHECKING:
    from .models import User, Restaurant


@dataclasses.dataclass
class UserDataClass:
    """Dataclass to represent serialized User model as class"""
    first_name: str
    last_name: str
    email: str
    restaurant: models.Restaurant = None
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
            restaurant=user.restaurant,
        )


@dataclasses.dataclass
class RestaurantDataClass:
    """Dataclass to represent serialized Restaurant model as class"""

    user: models.User
    name: str
    address: str
    description: str
    info_href: str
    id: int = None

    @classmethod
    def from_instance(cls, restaurant: "Restaurant") -> "RestaurantDataClass":
        return cls(
            user=restaurant.user,
            name=restaurant.name,
            address=restaurant.address,
            description=restaurant.description,
            info_href=restaurant.info_href,
            id=restaurant.id,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    """
    Method to create user
    :param user_dc: dataclass (dict) input, which uses to create models.User object
    :return: created object mapped back in the dataclass
    """
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
        is_staff=False,
        restaurant=None,
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)


def user_email_selector(email: str) -> "User":
    """
    Method to find exciting in database user by :param email:
    :return: User object
    """
    user = models.User.objects.filter(email=email).first()

    return user


def create_token(user_id: int) -> str:
    """
    Method to create JWT token for logining in user, using :param user_id:, current date&time and JWT_SECRET
    Created token expires after 24 hours from moment of creation

    :return: created token
    """
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
