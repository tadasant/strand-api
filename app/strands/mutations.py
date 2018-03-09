import graphene

from app.api.authorization import authorize
from app.strands.types import (
    StrandType,
    StrandInputType,
    TagType,
    TagInputType,
)
from app.strands.validators import StrandValidator, TagValidator


class CreateStrandMutation(graphene.Mutation):
    class Arguments:
        input = StrandInputType(required=True)

    strand = graphene.Field(StrandType)

    @authorize(raise_exception=True)
    def mutate(self, info, input):
        strand_validator = StrandValidator(data=input)
        strand_validator.is_valid(raise_exception=True)
        strand = strand_validator.save()
        return CreateStrandMutation(strand=strand)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    @authorize(raise_exception=True)
    def mutate(self, info, input):
        tag_validator = TagValidator(data=input)
        tag_validator.is_valid(raise_exception=True)
        tag = tag_validator.save()
        return CreateTagMutation(tag=tag)


class Mutation(graphene.ObjectType):
    create_strand = CreateStrandMutation.Field()
    create_tag = CreateTagMutation.Field()
