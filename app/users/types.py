import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_authorization
from app.groups.types import GroupType
from app.users.models import User


class UserType(DjangoObjectType):
    groups = graphene.List(GroupType)

    class Meta:
        model = User
        only_fields = ('id', 'email', 'messages', 'replies', 'topics', 'groups')

    @check_authorization
    def resolve_email(self, info):
        return self.email

    def resolve_groups(self, info):
        return self.strand_groups.all()


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    group_ids = graphene.List(graphene.Int)
