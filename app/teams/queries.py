import graphene

from app.teams.models import Team
from app.teams.types import TeamType


class Query(graphene.ObjectType):
    team = graphene.Field(TeamType, id=graphene.Int(), name=graphene.String())
    teams = graphene.List(TeamType)

    def resolve_team(self, info, id=None, name=None):
        if id is not None:
            return Team.objects.get(pk=id)
        if name is not None:
            return Team.objects.get(name=name)
        return None

    def resolve_teams(self, info):
        return Team.objects.all()
