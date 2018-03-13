import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import authorize
from app.strands.models import Strand, Tag


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        only_fields = ('id', 'name', 'strands',)

    @authorize(object_level=True)
    def resolve_id(self, info):
        return self.id

    @authorize(object_level=True)
    def resolve_name(self, info):
        return self.name

    @authorize(object_level=True)
    def resolve_strands(self, info):
        return self.strands


class StrandType(DjangoObjectType):
    class Meta:
        model = Strand
        only_fields = ('id', 'title', 'body', 'timestamp', 'original_poster', 'owner', 'tags', )

    @authorize(object_level=True)
    def resolve_id(self, info):
        return self.id

    @authorize(object_level=True)
    def resolve_title(self, info):
        return self.title

    @authorize(object_level=True)
    def resolve_body(self, info):
        return self.body

    @authorize(object_level=True)
    def resolve_timestamp(self, info):
        return self.timestamp

    @authorize(object_level=True)
    def resolve_original_poster(self, info):
        return self.original_poster

    @authorize(object_level=True)
    def resolve_owner(self, info):
        return self.owner

    @authorize(object_level=True)
    def resolve_tags(self, info):
        return self.tags


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class StrandInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    body = graphene.String(required=True)
    timestamp = graphene.String()
    original_poster_id = graphene.Int(required=True)
    owner_id = graphene.Int(required=True)
    tags = graphene.List(TagInputType)
