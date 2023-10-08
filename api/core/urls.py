"""Root URL routing"""
from django.contrib import admin
from django.urls import path, include

# To understand what the heck is /old/ check the .custom_middleware.py file
urlpatterns = [
    path('admin/', admin.site.urls),
    path('old/lunch/', include('menu_manager.urls')),
    path('lunch/', include('menu_manager.urls')),
    path('old/', include('user.urls')),
    path('', include('user.urls')),
]

urlpatterns += [
    path('api-auth', include('rest_framework.urls')),
]
