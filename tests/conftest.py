import re

import pytest
import responses
from pytest_factoryboy.fixture import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.factories import (
    TeamFactory,
    StrandFactory,
    TagFactory,
    UserFactory
)

register(TeamFactory)
register(StrandFactory)
register(TagFactory)
register(UserFactory)


@pytest.fixture()
def user_client(user_factory):
    """Pytest fixture for authenticated API client

    Most of our mutations require authentication. Rather than authenticate
    with a mock user each time, this fixture allows us to use an already
    authenticated api client.
    """
    user = user_factory()
    client = APIClient()
    token = Token.objects.get(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    setattr(client, 'user', user)
    return client


@pytest.fixture()
def superuser_client(user_factory):
    """Pytest fixture for authenticated API client

    Most of our mutations require authentication. Rather than authenticate
    with a mock user each time, this fixture allows us to use an already
    authenticated api client. We use a superuser that represents the
    permissions we would have when interacting with API from SLA.
    """
    user = user_factory(is_superuser=True)
    client = APIClient()
    token = Token.objects.get(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    setattr(client, 'user', user)
    return client


@pytest.fixture()
def algolia(mocker):
    request_mock = responses.RequestsMock(assert_all_requests_are_fired=False)
    request_mock.start()

    # Mock indexing
    request_mock.add(method=responses.PUT, url=re.compile(r'https://(.*?)/1/indexes/test_strands/\d+'),
                     json={})

    # Mock searching
    request_mock.add(method=responses.POST,
                     url=re.compile(r'https://(.*?)/1/indexes/test_strands/query'),
                     json={'hits': []})

    yield request_mock

    request_mock.stop()
    request_mock.reset()
