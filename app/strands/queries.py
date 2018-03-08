import graphene

from app.strands.models import Strand, Tag
from app.strands.types import StrandType, TagType


class Query(graphene.ObjectType):
    strand = graphene.Field(StrandType, id=graphene.Int())
    strands = graphene.List(StrandType)

    tag = graphene.Field(TagType, name=graphene.String())
    tags = graphene.List(TagType)

    def resolve_strand(self, info, id=None):
        if id:
            return Strand.objects.get(pk=id)
        return None

    def resolve_strands(self, info):
        return Strand.objects.all()

    def resolve_tag(self, info, name=None):
        if name:
            return Tag.objects.get(name=name)
        return None

    def resolve_tags(self, info):
        return Tag.objects.all()
