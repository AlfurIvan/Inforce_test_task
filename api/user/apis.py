from rest_framework import views, response, exceptions, permissions
from django.shortcuts import redirect

from . import serializer as user_serializer
from . import services
from . import authentication
from . import models


class RegisterApi(views.APIView):
    """
    API to register new user with unique email
    GET: hint to input
    POST: {first_name, last_name, email, password}
    :returns data same as input
    """
    # good to redirect to LoginAPI after

    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request):
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
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_user(user_dc=data)

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    """
    API to login exciting user
    GET: hint to input
    POST: {email, password}
    :returns empty response with jwt-token, which contains user ID
            and expires after 24 hours(look for services.create_token)

    """
    def get(self, request):
        # if "HTTP_VERSION" in request.headers:
        #     return redirect("/old/logout")
        return response.Response({'email': 'email', 'password': 'password'})

    def post(self, request):
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

    POST: nothing in payload

    kills the exciting token
    :returns message
    """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        if request.META.get["HTTP_VERSION"] == "1.0.0":
            return redirect("/old/logout")
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Cya)"}

        return resp


class UserApi(views.APIView):
    """
    This endpoint can only be used if user is authenticated

    GET::returns User object data
    """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        # if request.META.get["HTTP_VERSION"] == "1.0.0":
        #     redirect(f"/old/{self}")
        user = request.user
        obj = models.User.objects.prefetch_related("restaurant").filter(id=user.id).get()
        serializer = user_serializer.UserSerializer(obj)

        return response.Response(serializer.data)
