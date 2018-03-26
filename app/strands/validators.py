# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.api.authorization import check_permission_for_validator
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

    # TODO: Should probably check if user has view_team permissions
    # for the owner team before allowing him/her to add a strand
    @check_permission_for_validator('add_strand')
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        strand = super().create(validated_data)
        strand.set_tags(tags)
        return strand

    # TODO: Should probably check if user has view_team permissions
    # for the new owner team before allowing him/her to change a strand
    @check_permission_for_validator('change_strand')
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        strand = super().update(instance, validated_data)
        strand.set_tags(tags)
        return strand


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )

    @check_permission_for_validator('add_tag')
    def create(self, validated_data):
        tag = super().create(validated_data)
        return tag

    # TODO: We probably don't want to allow people to change tags
    # unless we add an owner field and make them non-public. This
    # isn't an issue right now because no-one has change_tag permissions.
    @check_permission_for_validator('change_tag')
    def update(self, instance, validated_data):
        tag = super().update(instance, validated_data)
        return tag


# TODO: [API-164] Implement delete
