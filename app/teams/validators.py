# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.teams.models import Team


class TeamValidator(serializers.ModelSerializer):
    # TODO: [API-157] FKs of users to include on creation

    class Meta:
        model = Team
        fields = ('id', 'name')

    def create(self, validated_data):
        # TODO: Check add_team permission
        team = super().create(**validated_data)
        return team

    def update(self, instance, validated_data):
        # TODO: Check change_team permission
        team = super().update(instance, validated_data)
        return team
