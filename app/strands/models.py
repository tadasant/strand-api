import algoliasearch_django
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils.timezone import now
from guardian.shortcuts import assign_perm
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
    """Add view_tag permissions to the default group"""
    if created:
        group = Group.objects.get(name=settings.DEFAULT_GROUP_NAME)
        assign_perm('view_tag', group, instance)


class Strand(TimeStampedModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField(default=now)

    saver = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name='strands')
    owner = models.ForeignKey(to=Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='strands')
    tags = models.ManyToManyField(to=Tag, related_name='strands')

    class Meta:
        permissions = (
            ('view_strand', 'View strand'),  # add_strand, change_strand, and delete_strand are added by default
        )

    def __str__(self):
        return self.title or f'Strand by {self.saver.email} from {self.owner.name}'

    def tag_names(self):
        return [tag.name for tag in self.tags.all()]

    def set_tags(self, tags):
        self.tags.clear()

        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            self.tags.add(tag)


@receiver(post_save, sender=Strand)
def assign_permissions(sender, instance, created, **kwargs):
    """Assign permissions to team group and user"""
    if created:
        assign_perm('view_strand', instance.owner.group, instance)
        assign_perm('change_strand', instance.saver, instance)
        assign_perm('delete_strand', instance.saver, instance)
        assign_perm('view_strand', instance.saver, instance)


@receiver(m2m_changed, sender=Strand.tags.through)
def update_algolia_index(sender, instance, action, **kwargs):
    """Force index to save record when tags are added or removed"""
    algoliasearch_django.save_record(instance)

    if action == 'post_clear':
        # Delete orphaned tags
        qs = Tag.objects.exclude(pk__in=Strand.tags.through.objects.values('tag'))
        qs.delete()


# TODO: [API-150] Receiver to delete orphans
# http://django-guardian.readthedocs.io/en/stable/userguide/caveats.html

# TODO: [API-160] Migration to add "add_strand" and "add_tag" permissions to users
# https://docs.djangoproject.com/en/2.0/topics/auth/default/#permissions-and-authorization
