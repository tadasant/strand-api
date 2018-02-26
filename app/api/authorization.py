from rest_framework.authentication import TokenAuthentication


def get_user(context):
    try:
        token_authentication = TokenAuthentication()
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


def check_topic_authorization(resolve_function):
    """
    Performs authorization checks for topics.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)

        if not self.is_private:
            return resolve_function(self, info, **kwargs)
        elif user and user.is_superuser:
            return resolve_function(self, info, **kwargs)
        else:
            return None
    return wrapper


def check_discussion_authorization(resolve_function):
    """
    Performs authorization checks for discussions.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)

        if not self.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif user and user.is_superuser:
            return resolve_function(self, info, **kwargs)
        else:
            return None
    return wrapper


def check_message_authorization(resolve_function):
    """
    Performs authorization checks for messages.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)

        if not self.discussion.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif user and user.is_superuser:
            return resolve_function(self, info, **kwargs)
        else:
            return None
    return wrapper


def check_reply_authorization(resolve_function):
    """
    Performs authorization checks for replies.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)

        if not self.message.discussion.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif user and user.is_superuser:
            return resolve_function(self, info, **kwargs)
        else:
            return None
    return wrapper
