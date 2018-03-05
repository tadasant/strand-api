import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_authorization
from app.groups.types import GroupType
from app.users.models import User


class UserType(DjangoObjectType):
    groups = graphene.List(GroupType)

    class Meta:
        model = User
        only_fields = ('id', 'alias', 'slack_users',
                       'messages', 'replies', 'topics',
                       'groups')

    @check_authorization
    def resolve_slack_users(self, info):
        return self.slack_users

    def resolve_groups(self, info):
        return self.strand_groups.all()


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    avatar_url = graphene.String()
    is_bot = graphene.Boolean()
    group_ids = graphene.List(graphene.Int)
