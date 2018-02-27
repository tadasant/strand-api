# Use of serializers limited to validating and saving models.

from rest_framework import serializers

from app.dialogues.models import Message, Reply
from app.topics.models import Discussion
from app.users.models import User


class MessageValidator(serializers.ModelSerializer):
    discussion_id = serializers.PrimaryKeyRelatedField(queryset=Discussion.objects.all(), source='discussion')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')

    class Meta:
        model = Message
        fields = ('id', 'text', 'discussion_id', 'author_id', 'time')

    def validate(self, data):
        if Discussion.objects.get(pk=data.get('discussion').id).is_closed:
            raise serializers.ValidationError('Cannot create message in closed discussion')
        return data


class ReplyValidator(serializers.ModelSerializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), source='message')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')

    class Meta:
        model = Reply
        fields = ('id', 'text', 'message_id', 'author_id', 'time')

    def validate(self, data):
        if Message.objects.get(pk=data.get('message').id).discussion.is_closed:
            raise serializers.ValidationError('Cannot create reply to message in closed discussion')
        return data
