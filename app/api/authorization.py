from rest_framework.authentication import TokenAuthentication
from django.db import models
from guardian.shortcuts import get_perms


def get_user(context):
    try:
        token_authentication = TokenAuthentication()
        # Will return None and raise TypeError if no auth header present
        user, token = token_authentication.authenticate(context)
    except TypeError:
        return None

    return user


def authorize(object_level=False, raise_exception=False):
    def check_authorization(resolve_function):
        """
        Performs authorization checks with django-guardian.

        Checks to see if the user is authenticated and has
        view permissions for the object requested.
        """
        def wrapper(self, info, **kwargs):
            user = get_user(info.context)

            if user and user.is_authenticated:
                if object_level and issubclass(self.__class__, models.Model):
                    if any('view_' in perm for perm in get_perms(user, self)):
                        return resolve_function(self, info, **kwargs)
                else:
                    return resolve_function(self, info, **kwargs)

            if raise_exception:
                raise Exception('Unauthorized')

            return None
        return wrapper
    return check_authorization
