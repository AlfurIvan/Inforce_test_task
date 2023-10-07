"""Menu and Order models"""
from django.db import models
from user import models as user_models


class Menu(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=1023)
    restaurant = models.ForeignKey(user_models.Restaurant, on_delete=models.SET(None), related_name='menus')


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.OneToOneField(user_models.User, on_delete=models.SET(None))
    selected_menu = models.OneToOneField(Menu, on_delete=models.SET(None))
