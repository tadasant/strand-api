from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
from guardian.shortcuts import assign_perm
from rest_framework.authtoken.models import Token


class User(AbstractUser, GuardianUserMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'),
                                max_length=150,
                                help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator])
    email = models.EmailField(_('email address'),
                              unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        permissions = (
            ('view_user', 'View user'),  # add_user, change_user and delete_user are added by default
        )

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token_and_add_permissions(sender, instance=None, created=False, **kwargs):
    """Create auth token, add to group and add appropriate permissions to new users."""
    if created:
        # Create token
        Token.objects.create(user=instance)

        # Add to public group
        group = Group.objects.get(name=settings.DEFAULT_GROUP_NAME)
        group.user_set.add(instance)
        # Assign permissions
        assign_perm('view_user', instance, instance)
        assign_perm('change_user', instance, instance)
        assign_perm('delete_user', instance, instance)

# TODO: Receiver to delete orphans
# http://django-guardian.readthedocs.io/en/stable/userguide/caveats.html
