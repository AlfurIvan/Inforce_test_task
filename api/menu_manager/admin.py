from django.contrib import admin

from .models import Menu, Order


class MenuAdmin(admin.ModelAdmin):
    """For readability in the django-admin"""
    list_display = ("id", "restaurant", "date", "description")


class OrderAdmin(admin.ModelAdmin):
    """For readability in the django-admin"""
    list_display = ("id", "user", "date", "selected_menu")


admin.site.register(Menu)
admin.site.register(Order)
