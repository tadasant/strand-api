from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from model_utils.models import TimeStampedModel

from app.users.models import User


class Team(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(to=User, related_name='teams')

    class Meta:
        permissions = (
            ('view_team', 'View team'),  # add_team, change_team and delete_team are added by default
        )

    def __str__(self):
        return self.name


@receiver(post_save, sender=Team)
def create_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.create(name=Team.name)
        assign_perm('view_team', group, Team)


@receiver(m2m_changed, sender=Team)
def update_group_membership(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        group = Group.objects.get(name=instance.name)
        group.user_set.remove(pk_set)
    elif action == 'post_remove':
        group = Group.objects.get(name=instance.name)
        group.user_set.add(pk_set)
    else:
        pass
