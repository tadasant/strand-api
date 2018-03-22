import graphene

from app.api.authorization import authenticate
from app.users.models import User
from app.users.types import (
    UserType,
    UserInputType,
    UserWithTeamsInputType,
    ChangePasswordInputType,
)
from app.users.validators import UserValidator


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)

    user = graphene.Field(UserType)

    @authenticate
    def mutate(self, info, input):
        user_validator = UserValidator(data=input, context=dict(request=info.context))
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()

        return CreateUserMutation(user=user)


class ChangePasswordMutation(graphene.Mutation):
    class Arguments:
        input = ChangePasswordInputType(required=True)

    user = graphene.Field(UserType)

    @authenticate
    def mutate(self, info, input):
        old_password, new_password = input.pop('old_password'), input.pop('new_password')

        user = User.objects.get(pk=input['id'])
        user_validator = UserValidator(instance=user, data=input, context=dict(request=info.context), partial=True)
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()

        if not user.check_password(old_password):
            raise Exception({'old_password': ['Wrong password.']})

        user.set_password(new_password)
        user.save()
        return ChangePasswordMutation(user=user)


class CreateUserWithTeamsMutation(graphene.Mutation):
    class Arguments:
        input = UserWithTeamsInputType(required=True)

    user = graphene.Field(UserType)

    @authenticate
    def mutate(self, info, input):
        user_validator = UserValidator(data=input, context=dict(request=info.context))
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()
        return CreateUserWithTeamsMutation(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    create_user_with_teams = CreateUserWithTeamsMutation.Field()
    change_password = ChangePasswordMutation.Field()
