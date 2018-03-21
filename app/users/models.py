from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
from guardian.shortcuts import assign_perm
from rest_framework.authtoken.models import Token


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Require email address to be set.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        """
        Make username optional.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, GuardianUserMixin):
    email = models.EmailField(_('email address'),
                              unique=True)
    password = models.CharField(_('password'), max_length=128, null=True, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'),
                                max_length=150,
                                help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                null=True,
                                blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_random_password_and_send_email(sender, instance=None, created=False, **kwargs):
    """Set random password and send user an email."""
    if created and not instance.password:
        # Generate random password
        password = User.objects.make_random_password(length=14)
        instance.set_password(password)
        instance.save()

        # Send email with password
        mail = EmailMultiAlternatives(
            subject='Welcome to Strand',
            body=f'Your password is "{password}"',
            from_email='Jacob Wallenberg <jacob@trystrand.com>',
            to=[instance.email],
            headers={},
        )
        mail.template_id = settings.NEW_ACCOUNT_TEMPLATE_ID
        mail.substitutions = {'%email%': instance.email,
                              '%password%': password}
        mail.attach_alternative(
            '<p><b>Welcome to Strand!</b></p>'
            f'<p>Your password is {password}</p>',
            'text/html'
        )
        mail.send()


# TODO: [API-150] Receiver to delete orphans
# http://django-guardian.readthedocs.io/en/stable/userguide/caveats.html
