import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import authorize
from app.teams.models import Team


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        only_fields = ('id', 'name', 'members', 'strands',)

    @authorize(object_level=True)
    def resolve_id(self, info):
        return self.id

    @authorize(object_level=True)
    def resolve_name(self, info):
        return self.name

    @authorize(object_level=True)
    def resolve_members(self, info):
        return self.members

    @authorize(object_level=True)
    def resolve_strands(self, info):
        return self.strands


class TeamInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
