# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group
from app.topics.models import Topic, Discussion, Tag
from app.users.models import User


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TopicValidator(serializers.ModelSerializer):
    original_poster_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='original_poster')
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='group')
    tags = serializers.ListField(required=False)

    class Meta:
        model = Topic
        fields = ('title', 'description', 'is_private', 'original_poster_id', 'group_id', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        topic = Topic.objects.create(**validated_data)
        topic.add_or_create_tags(tags)
        return topic


class DiscussionValidator(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), source='topic')

    class Meta:
        model = Discussion
        fields = ('id', 'status', 'time_start', 'time_end', 'topic_id')
