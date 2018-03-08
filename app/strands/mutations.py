import graphene

from app.api.authorization import check_authorization


class CreateStrandMutation(graphene.Mutation):
    pass


class CreateTagMutation(graphene.Mutation):
    pass


class Mutation(graphene.ObjectType):
    create_strand = CreateStrandMutation.Field()
    create_tag = CreateTagMutation.Field()
