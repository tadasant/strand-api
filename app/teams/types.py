import graphene
from graphene_django.types import DjangoObjectType

from app.teams.models import Team


class TeamType(DjangoObjectType):
    class Meta:
        model = Team


class TeamInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
