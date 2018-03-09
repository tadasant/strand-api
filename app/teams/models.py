from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm
from model_utils.models import TimeStampedModel

from app.users.models import User


def validate_team_name(name):
    """Public is the default group name"""
    if name == 'public':
        raise ValidationError(_('"public" is not a valid name.'))


class Team(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True, validators=validate_team_name)
    members = models.ManyToManyField(to=User, related_name='teams')
    group = models.OneToOneField(to=Group, related_name='team', on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('view_team', 'View team'),  # add_team, change_team and delete_team are added by default
        )

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Team)
def create_group(sender, instance, **kwargs):
    """Create group and assign to team"""
    group = Group.objects.create(name=instance.name)
    instance.group = group
    return instance


@receiver(post_save, sender=Team)
def assign_permissions(sender, instance, created, **kwargs):
    """Assign view_team permission to group"""
    if created:
        assign_perm('view_team', instance.group, Team)


@receiver(m2m_changed, sender=Team)
def update_group(sender, instance, action, pk_set, **kwargs):
    """Update group membership based on team members"""
    if action == 'post_add':
        # Get group for team and add new members to group
        group = Group.objects.get(name=instance.name)
        group.user_set.add(pk_set)
    elif action == 'post_remove':
        # Get group for team and remove old members from group
        group = Group.objects.get(name=instance.name)
        group.user_set.remove(pk_set)
