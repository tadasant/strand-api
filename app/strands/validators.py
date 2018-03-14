# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission
from app.strands.models import Strand, Tag
from app.teams.models import Team
from app.users.models import User


class StrandValidator(serializers.ModelSerializer):
    saver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='saver')
    owner_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='owner')
    tags = serializers.ListField(required=False)

    class Meta:
        model = Strand
        fields = ('title', 'body', 'timestamp', 'saver_id', 'owner_id', 'tags')

    @check_permission('add_strand')
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        strand = super().create(validated_data)
        strand.add_tags(tags)
        return strand

    @check_permission('change_strand')
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        strand = super().update(instance, validated_data)
        strand.add_tags(tags)
        return strand


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )

    @check_permission('add_tag')
    def create(self, validated_data):
        tag = super().create(validated_data)
        return tag

    @check_permission('change_tag')
    def update(self, instance, validated_data):
        tag = super().update(instance, validated_data)
        return tag


# TODO: [API-164] Implement delete
