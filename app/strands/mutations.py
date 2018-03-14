import graphene

from app.api.authorization import authenticate
from app.strands.models import Strand
from app.strands.types import (
    StrandType,
    StrandInputType,
    UpdateStrandInputType,
    TagType,
    TagInputType,
)
from app.strands.validators import StrandValidator, TagValidator


class CreateStrandMutation(graphene.Mutation):
    class Arguments:
        input = StrandInputType(required=True)

    strand = graphene.Field(StrandType)

    @authenticate
    def mutate(self, info, input):
        strand_validator = StrandValidator(data=input, context={'request': info.context})
        strand_validator.is_valid(raise_exception=True)
        strand = strand_validator.save()
        return CreateStrandMutation(strand=strand)


class UpdateStrandMutation(graphene.Mutation):
    class Arguments:
        input = UpdateStrandInputType(required=True)

    strand = graphene.Field(StrandType)

    @authenticate
    def mutate(self, info, input):
        strand = Strand.objects.get(id=input.pop('id'))
        strand_validator = StrandValidator(instance=strand, data=input, context={'request': info.context}, partial=True)
        strand_validator.is_valid(raise_exception=True)
        strand = strand_validator.save()
        return UpdateStrandMutation(strand=strand)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    @authenticate
    def mutate(self, info, input):
        tag_validator = TagValidator(data=input, context={'request': info.context})
        tag_validator.is_valid(raise_exception=True)
        tag = tag_validator.save()
        return CreateTagMutation(tag=tag)


class Mutation(graphene.ObjectType):
    create_strand = CreateStrandMutation.Field()
    update_strand = UpdateStrandMutation.Field()
    create_tag = CreateTagMutation.Field()
