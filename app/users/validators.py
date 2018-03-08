# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group
from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    group_ids = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'group_ids')

    def create(self, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        user = User.objects.create(**validated_data)
        user.add_to_groups(group_ids)
        return user
