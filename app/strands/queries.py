import graphene
from algoliasearch_django import raw_search

from app.strands.models import Strand, Tag
from app.strands.types import StrandType, TagType


class Query(graphene.ObjectType):
    strand = graphene.Field(StrandType, id=graphene.Int())
    strands = graphene.List(StrandType)

    search = graphene.List(StrandType,
                           query=graphene.String(required=True),
                           size=graphene.Int(required=False),
                           page=graphene.Int(required=False))

    tag = graphene.Field(TagType, name=graphene.String())
    tags = graphene.List(TagType)

    def resolve_strand(self, info, id=None):
        if id:
            return Strand.objects.get(pk=id)
        return None

    def resolve_strands(self, info):
        return Strand.objects.all()

    def resolve_search(self, info, query, size=100, page=0):
        # TODO: Incorporate permissions into indices for efficiency
        results = raw_search(Strand, query=query, params={'hitsPerPage': size, 'page': page})
        return Strand.objects.filter(id__in=map(lambda x: x['objectID'], results['hits'])).all()

    def resolve_tag(self, info, name=None):
        if name:
            return Tag.objects.get(name=name)
        return None

    def resolve_tags(self, info):
        return Tag.objects.all()
