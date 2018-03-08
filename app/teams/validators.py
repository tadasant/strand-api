# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.teams.models import Team


class TeamValidator(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
