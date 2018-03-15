# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission_for_validator
from app.users.models import User
from app.teams.models import Team
from app.teams.validators import TeamValidator


class UserValidator(serializers.ModelSerializer):
    team_ids = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'team_ids')

    @check_permission_for_validator('add_user')
    def create(self, validated_data):
        teams = validated_data.pop('team_ids', [])
        user = super().create(validated_data)

        for team in teams:
            # Use team validator to handle permission checks
            team_validator = TeamValidator(instance=team, data=dict(member_ids=[user.id]),
                                           context=dict(request=self.context['request'], member_operation='add'),
                                           partial=True)
            team_validator.is_valid(raise_exception=True)
            team_validator.save()
        return user

    @check_permission_for_validator('change_user')
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user


# TODO: [API-164] Implement delete
