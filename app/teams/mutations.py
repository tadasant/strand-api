import graphene

from app.api.authorization import authorize
from app.teams.validators import TeamValidator
from app.teams.types import TeamType, TeamInputType


class CreateTeamMutation(graphene.Mutation):
    class Arguments:
        input = TeamInputType(required=True)

    team = graphene.Field(TeamType)

    # TODO: [API-153] Move to authorization to model
    @authorize(raise_exception=True)
    def mutate(self, info, input):
        team_validator = TeamValidator(data=input, context={'context': info.context})
        team_validator.is_valid(raise_exception=True)
        team = team_validator.save()

        return CreateTeamMutation(team=team)


class Mutation(graphene.ObjectType):
    create_team = CreateTeamMutation.Field()
