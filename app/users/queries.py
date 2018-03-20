import graphene

from app.api.authorization import authenticate
from app.users.models import User
from app.users.types import UserType


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(), email=graphene.String())
    users = graphene.List(UserType)

    @authenticate
    def resolve_me(self, info):
        if info.context.user and info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_user(self, info, id=None, email=None):
        if id is not None:
            return User.objects.get(pk=id)

        if email is not None:
            return User.objects.get(email=email)
        return None

    def resolve_users(self, info):
        return User.objects.all()
