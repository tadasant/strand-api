import graphene

from app.api.authorization import check_authorization
from app.strands.types import (
    StrandType,
    StrandInputType,
    TagType,
    TagInputType,
)


class CreateStrandMutation(graphene.Mutation):
    class Arguments:
        input = StrandInputType(required=True)

    strand = graphene.Field(StrandType)

    @check_authorization
    def mutate(self, info, input):
        return CreateStrandMutation(strand=None)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    @check_authorization
    def mutate(self, info, input):
        return CreateTagMutation(tag=None)


class Mutation(graphene.ObjectType):
    create_strand = CreateStrandMutation.Field()
    create_tag = CreateTagMutation.Field()
