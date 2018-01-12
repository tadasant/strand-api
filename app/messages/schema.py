import graphene
from graphene_django.types import DjangoObjectType

from app.messages.models import Message, Reply


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply


class Query(graphene.ObjectType):
    message = graphene.Field(MessageType, id=graphene.Int())
    reply = graphene.Field(ReplyType, id=graphene.Int())

    messages = graphene.List(MessageType)
    replies = graphene.List(ReplyType)

    def resolve_message(self, info, id=None):
        if id is not None:
            return Message.objects.get(pk=id)

        return None

    def resolve_reply(self, info, id=None):
        if id is not None:
            return Reply.objects.get(pk=id)

        return None

    def resolve_messages(self, info):
        return Message.objects.all()

    def resolve_replies(self, info):
        return Reply.objects.all()