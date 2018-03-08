import graphene
from django.db.models import Q
from django.conf import settings

from app.users.models import User
from app.users.types import UserType


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, id=None):
        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info):
        # Django guardian needs an anonymous user to handle permissions
        return User.objects.filter(~Q(email=settings.ANONYMOUS_USER_NAME)).all()
