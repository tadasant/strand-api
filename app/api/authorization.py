from rest_framework.authentication import TokenAuthentication
from app.topics.models import Topic, Discussion
from app.dialogues.models import Message, Reply


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


def check_topic_authorization(resolve_function):
    """
    Performs authorization checks for topics.
    """
    def wrapper(self, info, **kwargs):
        user = get_user(info.context)

        if isinstance(self, Topic) and not self.is_private:
            return resolve_function(self, info, **kwargs)
        elif isinstance(self, Discussion) and not self.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif isinstance(self, Message) and not self.discussion.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif isinstance(self, Reply) and not self.message.discussion.topic.is_private:
            return resolve_function(self, info, **kwargs)
        elif user and user.is_superuser:
            return resolve_function(self, info, **kwargs)
        else:
            return None
    return wrapper
