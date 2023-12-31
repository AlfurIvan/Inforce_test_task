"""URL routing for User-related actions"""
from django.urls import path

from . import apis

urlpatterns = [
    path("register/", apis.RegisterApi.as_view(), name="register"),
    path("login/", apis.LoginApi.as_view(), name="login"),
    path("", apis.UserApi.as_view(), name="cabinet"),
    path("logout/", apis.LogoutApi.as_view(), name="logout"),
]
