from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    """For readability in the django-admin"""
    list_display = ("id", "first_name", "last_name", "email")


class RestaurantAdmin(admin.ModelAdmin):
    """For readability in the django-admin"""
    list_display = ("name", "user")


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Restaurant, RestaurantAdmin)
