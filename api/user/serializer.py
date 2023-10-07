"""User and Restaurant serialisation module"""
from rest_framework import serializers

from . import services


class RestaurantSerializer(serializers.Serializer):
    """Serialises models.Restaurant object"""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    description = serializers.CharField()
    info_href = serializers.CharField()

    def to_internal_value(self, data):
        """return model object"""
        data = super().to_internal_value(data)
        return services.RestaurantDataClass(**data)


class UserSerializer(serializers.Serializer):
    """Serialises models.User object"""
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    company = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        """return model object"""
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)
