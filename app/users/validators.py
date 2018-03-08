# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
