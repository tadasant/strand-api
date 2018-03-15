import graphene

from app.api.authorization import authenticate
from app.teams.models import Team
from app.teams.validators import TeamValidator
from app.teams.types import (
    TeamType,
    TeamInputType,
    AddMembersToTeamInputType
)


class CreateTeamMutation(graphene.Mutation):
    class Arguments:
        input = TeamInputType(required=True)

    team = graphene.Field(TeamType)

    @authenticate
    def mutate(self, info, input):
        team_validator = TeamValidator(data=input, context={'request': info.context})
        team_validator.is_valid(raise_exception=True)
        team = team_validator.save()

        return CreateTeamMutation(team=team)


class AddMembersToTeamMutation(graphene.Mutation):
    class Arguments:
        input = AddMembersToTeamInputType(required=True)

    team = graphene.Field(TeamType)

    @authenticate
    def mutate(self, info, input):
        team = Team.objects.get(id=input.pop('id'))
        team_validator = TeamValidator(instance=team, data=input, context={'request': info.context,
                                                                           'member_operation': 'add'}, partial=True)
        team_validator.is_valid(raise_exception=True)
        team = team_validator.save()

        return AddMembersToTeamMutation(team=team)


class Mutation(graphene.ObjectType):
    create_team = CreateTeamMutation.Field()
    add_members_to_team = AddMembersToTeamMutation.Field()
