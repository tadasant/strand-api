import pytz
from datetime import datetime, timedelta

import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateMessage:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory()
        message = message_factory.build(discussion=discussion, author=user)

        mutation = MutationGenerator.create_message(message.text, discussion.id, user.id, message.time)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessage'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_closed_discussion(self, auth_client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory(topic__is_private=False, status='CLOSED')
        user = user_factory()
        message = message_factory.build(discussion=discussion, author=user)

        mutation = MutationGenerator.create_message(message.text, discussion.id, user.id, message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessage'] is None
        assert response.json()['errors'][0]['message'] == "{'non_field_errors': ['Cannot create message in closed " \
                                                          "discussion']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory()
        message = message_factory.build(discussion=discussion, author=user)

        mutation = MutationGenerator.create_message(message.text, discussion.id, user.id, message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessage']['message']['text'] == message.text

    @pytest.mark.django_db()
    def test_marks_discussion_as_open(self, auth_client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory()
        message_factory(time=datetime.now(tz=pytz.UTC) - timedelta(minutes=31), discussion=discussion)
        discussion.mark_as_stale()
        discussion.save()

        message = message_factory.build(discussion=discussion, author=user)

        mutation = MutationGenerator.create_message(message.text, discussion.id, user.id, message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessage']['message']['text'] == message.text
        assert response.json()['data']['createMessage']['message']['discussion']['status'] == 'OPEN'
