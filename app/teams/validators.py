# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission_for_validator
from app.teams.models import Team


class TeamValidator(serializers.ModelSerializer):
    # TODO: [API-157] FKs of users to include on creation

    class Meta:
        model = Team
        fields = ('id', 'name')

    @check_permission_for_validator('add_team')
    def create(self, validated_data):
        team = super().create(validated_data)
        return team

    @check_permission_for_validator('change_team')
    def update(self, instance, validated_data):
        team = super().update(instance, validated_data)
        return team


# TODO: [API-164] Implement delete
