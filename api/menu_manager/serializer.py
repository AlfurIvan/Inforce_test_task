from rest_framework import serializers

from user import serializer as user_serializer


class MenuSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    description = serializers.CharField()
    restaurant = user_serializer.RestaurantSerializer()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    user = user_serializer.UserSerializer()
    selected_menu = MenuSerializer()
