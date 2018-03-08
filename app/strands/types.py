import graphene
from graphene_django.types import DjangoObjectType

from app.strands.models import Strand, Tag


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        only_fields = ('id', 'name', 'strands',)


class StrandType(DjangoObjectType):
    class Meta:
        model = Strand
        only_fields = ('id', 'title', 'body', 'timestamp', 'original_poster', 'owner', 'tags', )


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class StrandInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    body = graphene.String(required=True)
    timestamp = graphene.String()
    original_poster_id = graphene.Int(required=True)
    owner_id = graphene.Int(required=True)
    tags = graphene.List(TagInputType)
