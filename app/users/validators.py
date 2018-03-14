# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission_for_validator
from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)

    @check_permission_for_validator('add_user')
    def create(self, validated_data):
        user = super().create(validated_data)
        return user

    @check_permission_for_validator('change_user')
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user


# TODO: [API-164] Implement delete
