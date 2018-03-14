import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_permission_for_resolver
from app.strands.models import Strand, Tag


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        only_fields = ('id', 'name', 'strands',)

    @check_permission_for_resolver('view_tag')
    def resolve_id(self, info):
        return self.id

    @check_permission_for_resolver('view_tag')
    def resolve_name(self, info):
        return self.name

    @check_permission_for_resolver('view_tag')
    def resolve_strands(self, info):
        return self.strands


class StrandType(DjangoObjectType):
    class Meta:
        model = Strand
        only_fields = ('id', 'title', 'body', 'timestamp', 'saver', 'owner', 'tags', )

    @check_permission_for_resolver('view_strand')
    def resolve_id(self, info):
        return self.id

    @check_permission_for_resolver('view_strand')
    def resolve_title(self, info):
        return self.title

    @check_permission_for_resolver('view_strand')
    def resolve_body(self, info):
        return self.body

    @check_permission_for_resolver('view_strand')
    def resolve_timestamp(self, info):
        return self.timestamp

    @check_permission_for_resolver('view_strand')
    def resolve_saver(self, info):
        return self.saver

    @check_permission_for_resolver('view_strand')
    def resolve_owner(self, info):
        return self.owner

    @check_permission_for_resolver('view_strand')
    def resolve_tags(self, info):
        return self.tags


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class StrandInputType(graphene.InputObjectType):
    title = graphene.String()
    body = graphene.String(required=True)
    timestamp = graphene.String()
    saver_id = graphene.Int(required=True)
    owner_id = graphene.Int(required=True)
    tags = graphene.List(TagInputType)
