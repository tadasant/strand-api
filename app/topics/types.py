import graphene
from graphene_django.types import DjangoObjectType

from app.topics.models import Topic, Discussion, Tag
from app.api.authorization import check_topic_authorization


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        only_fields = ('id', 'title', 'description', 'is_private', 'original_poster', 'group', 'tags', 'discussion',)

    # TODO: Move to object-level permissions
    @check_topic_authorization
    def resolve_id(self, info):
        return self.id

    @check_topic_authorization
    def resolve_title(self, info):
        return self.title

    @check_topic_authorization
    def resolve_description(self, info):
        return self.description

    @check_topic_authorization
    def resolve_is_private(self, info):
        return self.is_private

    @check_topic_authorization
    def resolve_original_poster(self, info):
        return self.original_poster

    @check_topic_authorization
    def resolve_group(self, info):
        return self.group

    @check_topic_authorization
    def resolve_tags(self, info):
        return self.tags

    @check_topic_authorization
    def resolve_discussion(self, info):
        return self.discussion


class DiscussionType(DjangoObjectType):
    class Meta:
        model = Discussion
        only_fields = ('id', 'time_start', 'time_end', 'status', 'topic', 'participants',)

    # TODO: Move to object-level permissions
    @check_topic_authorization
    def resolve_id(self, info):
        return self.id

    @check_topic_authorization
    def resolve_time_start(self, info):
        return self.time_start

    @check_topic_authorization
    def resolve_time_end(self, info):
        return self.time_end

    @check_topic_authorization
    def resolve_status(self, info):
        return self.status

    @check_topic_authorization
    def resolve_topic(self, info):
        return self.topic

    @check_topic_authorization
    def resolve_participants(self, info):
        return self.participants


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class TopicInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_private = graphene.Boolean()
    original_poster_id = graphene.Int(required=True)
    group_id = graphene.Int()
    tags = graphene.List(TagInputType)


class DiscussionInputType(graphene.InputObjectType):
    time_start = graphene.String()
    time_end = graphene.String()
    topic_id = graphene.Int(required=True)


class TopicAndTagsInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_private = graphene.Boolean()
    original_poster_id = graphene.Int(required=True)


class MarkDiscussionAsPendingClosedInputType(graphene.InputObjectType):
    id = graphene.Int()


class CloseDiscussionInputType(graphene.InputObjectType):
    id = graphene.Int()
