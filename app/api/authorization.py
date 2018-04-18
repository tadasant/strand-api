import inspect

from rest_framework.authentication import TokenAuthentication


def get_user(context):
    """Gets the user based on the Authorization header.

    Takes the Authorization header and extracts the token.
    Uses the token to identify which user is making the request.
    """
    try:
        token_authentication = TokenAuthentication()
        # Will return None and raise TypeError if no auth header present
        user, token = token_authentication.authenticate(context)
    except TypeError:
        return None

    return user


def authenticate(resolve_function):
    """Authenticates a user given the GraphQL context.

    This is a decorator that is used on mutation methods.
    It allows us to access the user from the context parameter.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)
        setattr(info.context, 'user', user)

        return resolve_function(self, info, **kwargs)
    return wrapper


def check_permission_for_validator(permission_name):
    def wrap_validator_function(validator_function):
        """
        Performs authorization checks with django-guardian on validator methods.

        Checks to see if the user is authenticated and has add/change/delete
        permissions for the model or object.
        """
        def wrapper(self, *args):
            user = self.context['request'].user
            param_dict = dict(zip(list(inspect.signature(validator_function).parameters.keys()), args))

            if user and user.is_authenticated and user.has_perm(permission_name, param_dict.get('instance')):
                return validator_function(self, *args)

            raise Exception('Unauthorized')
        return wrapper
    return wrap_validator_function


def check_permission_for_resolver(permission_name):
    def wrap_resolve_function(resolve_function):
        """
        Performs authorization checks with django-guardian on resolver methods.

        Checks to see if the user is authenticated and has view permissions
        for the object requested.
        """
        def wrapper(self, info, **kwargs):
            user = get_user(info.context)

            if user and user.is_authenticated and user.has_perm(permission_name, self):
                return resolve_function(self, info, **kwargs)

            raise Exception('Unauthorized')
        return wrapper
    return wrap_resolve_function
