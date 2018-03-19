import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_permission_for_resolver
from app.users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'email', 'first_name', 'last_name', 'teams', 'strands',)

    @check_permission_for_resolver('view_user')
    def resolve_id(self, info):
        return self.id

    @check_permission_for_resolver('view_user')
    def resolve_email(self, info):
        return self.email

    @check_permission_for_resolver('view_user')
    def resolve_first_name(self, info):
        return self.first_name

    @check_permission_for_resolver('view_user')
    def resolve_last_name(self, info):
        return self.last_name

    @check_permission_for_resolver('view_user')
    def resolve_teams(self, info):
        return self.teams.all()

    @check_permission_for_resolver('view_user')
    def resolve_strands(self, info):
        return self.strands.all()


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
