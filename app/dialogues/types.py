import graphene
from graphene_django.types import DjangoObjectType

from app.dialogues.models import Message, Reply
from app.api.authorization import check_topic_authorization


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        only_fields = ('id', 'text', 'discussion', 'author', 'time', 'origin_slack_event',)

    # TODO: Move to object-level permissions
    @check_topic_authorization
    def resolve_id(self, info):
        return self.id

    @check_topic_authorization
    def resolve_text(self, info):
        return self.text

    @check_topic_authorization
    def resolve_discussion(self, info):
        return self.discussion

    @check_topic_authorization
    def resolve_author(self, info):
        return self.author

    @check_topic_authorization
    def resolve_time(self, info):
        return self.time

    @check_topic_authorization
    def resolve_origin_slack_event(self, info):
        return self.origin_slack_event


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply
        only_fields = ('id', 'text', 'message', 'author', 'time', 'origin_slack_event',)

    # TODO: Move to object-level permissions
    @check_topic_authorization
    def resolve_id(self, info):
        return self.id

    @check_topic_authorization
    def resolve_text(self, info):
        return self.text

    @check_topic_authorization
    def resolve_message(self, info):
        return self.message

    @check_topic_authorization
    def resolve_author(self, info):
        return self.author

    @check_topic_authorization
    def resolve_time(self, info):
        return self.time

    @check_topic_authorization
    def resolve_origin_slack_event(self, info):
        return self.origin_slack_event


class MessageInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    discussion_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)


class ReplyInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    message_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)
