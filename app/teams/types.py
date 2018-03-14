import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_view_permission
from app.teams.models import Team


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        only_fields = ('id', 'name', 'members', 'strands',)

    @check_view_permission('view_team')
    def resolve_id(self, info):
        return self.id

    @check_view_permission('view_team')
    def resolve_name(self, info):
        return self.name

    @check_view_permission('view_team')
    def resolve_members(self, info):
        return self.members

    @check_view_permission('view_team')
    def resolve_strands(self, info):
        return self.strands


class TeamInputType(graphene.InputObjectType):
    # TODO: [API-157] FKs of users to include on creation
    name = graphene.String(required=True)
