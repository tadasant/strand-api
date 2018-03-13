import graphene

from app.api.authorization import authenticate
from app.users.types import UserInputType, UserType
from app.users.validators import UserValidator


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)

    user = graphene.Field(UserType)

    @authenticate
    def mutate(self, info, input):
        user_validator = UserValidator(data=input, context={'request': info.context})
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()

        return CreateUserMutation(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
