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
        # TODO: Check add_strand permission
        tags = validated_data.pop('tags', [])
        strand = super().create(validated_data)
        strand.add_tags(tags)
        return strand

    def update(self, instance, validated_data):
        # TODO: Check change_strand permission
        tags = validated_data.pop('tags', [])
        strand = super().update(instance, validated_data)
        strand.add_tags(tags)
        return strand


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )

    def create(self, validated_data):
        # TODO: Check add_tag permission
        tag = super().create(validated_data)
        return tag

    def update(self, instance, validated_data):
        # TODO: Check change_tag permission
        tag = super().update(instance, validated_data)
        return tag
