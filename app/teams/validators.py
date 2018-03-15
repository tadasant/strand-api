# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission_for_validator
from app.teams.models import Team
from app.users.models import User


class TeamValidator(serializers.ModelSerializer):
    # TODO: [API-157] FKs of users to include on creation
    member_ids = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'member_ids')

    @check_permission_for_validator('add_team')
    def create(self, validated_data):
        team = super().create(validated_data)
        return team

    @check_permission_for_validator('change_team')
    def update(self, instance, validated_data):
        members = validated_data.pop('member_ids', [])
        team = super().update(instance, validated_data)

        # For the addMembersToTeam mutation, we just want to "add" members.
        if self.context['member_operation'] == 'add':
            team.members.add(*members)
        # If we add an update team mutation, we'll want to "set" the members.
        elif self.context['member_operation'] == 'set':
            team.members.set(*members)

        return team


# TODO: [API-164] Implement delete
