import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_authorization
from app.teams.types import TeamType
from app.users.models import User


class UserType(DjangoObjectType):
    teams = graphene.List(TeamType)

    class Meta:
        model = User
        only_fields = ('id', 'email', 'teams')

    @check_authorization
    def resolve_email(self, info):
        return self.email

    def resolve_teams(self, info):
        return self.teams.all()


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
