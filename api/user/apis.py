"""User APIs"""
from rest_framework import views, response, exceptions, permissions
from django.db import IntegrityError

from . import serializer as user_serializer
from . import services
from . import authentication
from . import models


class RegisterApi(views.APIView):
    """
    API to register new user with unique email
    New user can be created only by person with admin privileges
    """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request):
        """hint what to input"""
        return response.Response(
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@gmail.com",
                "password": "123123",
                "company": "ABC"
            }
        )

    def post(self, request):
        """
        Validation & creation new user
        :returns data same as input
        """
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            serializer.instance = services.create_user(user_dc=data)
        except IntegrityError:
            return response.Response({"error": "Already claimed email"})
        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    """
    API to login exciting user and return JWT token
    """
    def get(self, request):
        """hint what to input"""
        return response.Response({'email': 'email', 'password': 'password'})

    def post(self, request):
        """
        returns empty response with jwt-token, which contains user ID
        and expires after 24 hours(look for services.create_token)
        """
        exception = exceptions.AuthenticationFailed("Invalid credentials.")

        try:
            email = request.data["email"]
            password = request.data["password"]
        except KeyError:
            raise exception

        user = services.user_email_selector(email=email)

        if user is None:
            raise exception
        if not user.check_password(raw_password=password):
            raise exception

        token = services.create_token(user_id=user.id)
        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp


class LogoutApi(views.APIView):
    """
    API to logout user
    kills the exciting JWT token
    :returns just message
    """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        """Empty POST request to delete JWT token and end current session"""
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Cya)"}
        return resp


class UserApi(views.APIView):
    """
    Endpoint to retrieve current user data
    """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        """:returns User data"""
        user = request.user
        obj = models.User.objects.prefetch_related("restaurant").filter(id=user.id).get()
        serializer = user_serializer.UserSerializer(obj)

        try:
            serializer_rest = user_serializer.RestaurantSerializer(obj.restaurant)
            return response.Response({"user": serializer.data, "restaurant": serializer_rest.data})
        except AttributeError:
            return response.Response({"user": serializer.data})
