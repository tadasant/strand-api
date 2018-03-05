import graphene

from app.api.authorization import check_authorization
from app.dialogues.validators import MessageValidator, ReplyValidator
from app.dialogues.types import (
    MessageType,
    ReplyType,
    MessageInputType,
    ReplyInputType,
    UserAndMessageInputType,
    UserAndReplyInputType
)
from app.users.types import UserType
from app.users.validators import UserValidator


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        input = MessageInputType(required=True)

    message = graphene.Field(MessageType)

    @check_authorization
    def mutate(self, info, input):
        message_validator = MessageValidator(data=input)
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()
        return CreateMessageMutation(message=message)


class CreateUserAndMessageMutation(graphene.Mutation):
    class Arguments:
        input = UserAndMessageInputType(required=True)

    user = graphene.Field(UserType)
    message = graphene.Field(MessageType)

    @check_authorization
    def mutate(self, info, input):
        user_validator = UserValidator(data=input.pop('user'))
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()

        message_validator = MessageValidator(data=dict(author_id=user.id, **input.pop('message')))
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()
        return CreateUserAndMessageMutation(user=user, message=message)


class CreateReplyMutation(graphene.Mutation):
    class Arguments:
        input = ReplyInputType(required=True)

    reply = graphene.Field(ReplyType)

    @check_authorization
    def mutate(self, info, input):
        reply_validator = ReplyValidator(data=input)
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()
        return CreateReplyMutation(reply=reply)


class CreateUserAndReplyMutation(graphene.Mutation):
    class Arguments:
        input = UserAndReplyInputType(required=True)

    user = graphene.Field(UserType)
    reply = graphene.Field(ReplyType)

    @check_authorization
    def mutate(self, info, input):
        user_validator = UserValidator(data=input.pop('user'))
        user_validator.is_valid(raise_exception=True)
        user = user_validator.save()

        reply_validator = ReplyValidator(data=dict(author_id=user.id, **input.pop('reply')))
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()
        return CreateUserAndReplyMutation(user=user, reply=reply)


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_reply = CreateReplyMutation.Field()

    create_user_and_message = CreateUserAndMessageMutation.Field()
    create_user_and_reply = CreateUserAndReplyMutation.Field()
