from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
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
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create auth token for new users.

    Fires on post_save signal from users. Only creates
    token if post_save is result of new user being created.
    Note: Signal receivers must accept keyword arguments.
    """
    if created:
        Token.objects.create(user=instance)
