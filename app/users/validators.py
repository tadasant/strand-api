# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)

    def create(self, validated_data):
        # TODO: check add_user permissions
        print(self.context['request'].user)
        user = super().create(validated_data)
        return user

    def update(self, instance, validated_data):
        # TODO: check change_user permission
        print(self.context['request'].user)
        user = super().update(instance, validated_data)
        return user
