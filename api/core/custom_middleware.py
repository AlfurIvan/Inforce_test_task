"""Custom Middleware"""
from django.shortcuts import redirect
from . import settings


class VersionHeaderMiddleware:
    """
    This middleware is fetching user's app version from X-Frontend-Version header
    If user have version which is NOT EQUAL to newest (defined in settings, also may be defined in .env-s)
    he is going be redirected on the same functional route but with /old/ on the beginning.

    If user have the newest version, or somehow :request: does not have X-Frontend-Version header,
    user will receive the response like version is newest
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        version = request.headers.get('X-Frontend-Version')
        request.version_header = version
        if version:
            if version != settings.NEWEST_USERS_APP_VERSION and not request.path.startswith('/old/'):
                return redirect('/old' + request.path)

        return self.get_response(request)
