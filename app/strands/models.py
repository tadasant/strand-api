from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.timezone import now
from guardian.shortcuts import assign_perm
from guardian.utils import get_anonymous_user
from model_utils.models import TimeStampedModel

from app.teams.models import Team
from app.users.models import User


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        permissions = (
            ('view_tag', 'View tag'),  # add_tag, change_tag and delete_tag are added by default
        )

    def __str__(self):
        return self.name


@receiver(post_save, sender=Tag)
def add_view_permissions(sender, instance, created, **kwargs):
    if created:
        anonymous_user = get_anonymous_user()
        assign_perm('view_tag', anonymous_user, instance)
        # TODO: Add to default users group?


# TODO: Assign view permission to all users
# TODO: Assign add permission to all users


class Strand(TimeStampedModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(default=now)

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='strands')
    owner = models.ForeignKey(to=Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='strands')
    tags = models.ManyToManyField(to=Tag, related_name='strands')

    class Meta:
        permissions = (
            ('view_strand', 'View strand'),  # add_strand, change_strand, and delete_strand are added by default
        )

    def __str__(self):
        return self.title

    def add_tags(self, tags):
        for tag_to_add in tags:
            tag, _ = Tag.objects.get_or_create(**tag_to_add)
            self.tags.add(tag)

# TODO: Assign add permission to group of team
# TODO: Assign delete permission to group of team
# TODO: Assign change permission to group of team
# TODO: Assign view permission to group of team
