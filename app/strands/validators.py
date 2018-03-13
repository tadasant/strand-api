# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.teams.models import Team
from app.strands.models import Strand, Tag
from app.users.models import User


class StrandValidator(serializers.ModelSerializer):
    saver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='saver')
    owner_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='owner')
    tags = serializers.ListField(required=False)

    class Meta:
        model = Strand
        fields = ('title', 'body', 'timestamp', 'saver_id', 'owner_id', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        strand = Strand.objects.create(**validated_data)
        strand.add_tags(tags)
        return strand


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )
