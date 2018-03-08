import pytest
from pytest_factoryboy.fixture import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.factories import (
    GroupFactory,
    MessageFactory,
    TopicFactory,
    ReplyFactory,
    DiscussionFactory,
    TagFactory,
    UserFactory
)

register(GroupFactory)
register(MessageFactory)
register(TopicFactory)
register(ReplyFactory)
register(DiscussionFactory)
register(TagFactory)
register(UserFactory)


@pytest.fixture()
def auth_client(user_factory):
    """Pytest fixture for authenticated API client

    Most of our mutations require authentication. Rather than authenticate
    with a mock user each time, this fixture allows us to use an already
    authenticated api client.
    """
    user = user_factory()
    client = APIClient()
    token = Token.objects.get(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client
