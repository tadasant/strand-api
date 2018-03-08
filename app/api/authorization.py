from rest_framework.authentication import TokenAuthentication


def get_user(context):
    try:
        token_authentication = TokenAuthentication()
        # Will return None and raise TypeError if no auth header present
        user, token = token_authentication.authenticate(context)
    except TypeError:
        return None

    return user


def check_authorization(resolve_function):
    """
    Performs authorization checks for type fields.

    Checks to see if info.context.user.is_authenticated
    is true. If so, the resolve function is called. If
    false, an exception is raised.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)
        if user and user.is_authenticated:
            return resolve_function(self, info, **kwargs)
        else:
            raise Exception('Unauthorized')
    return wrapper
