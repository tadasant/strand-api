import pytz
from datetime import datetime, timedelta

import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateReply:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, reply_factory):
        message = message_factory()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_reply(reply.text, reply.message.id, message.author.id, reply.time)
        response = client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_closed_discussion(self, auth_client, discussion_factory, message_factory, reply_factory):
        discussion = discussion_factory(status='CLOSED')
        message = message_factory(discussion=discussion)
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_reply(reply.text, reply.message.id, message.author.id, reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createReply'] is None
        assert response.json()['errors'][0]['message'] == "{'non_field_errors': ['Cannot create reply to message in " \
                                                          "closed discussion']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, reply_factory):
        message = message_factory(discussion__topic__is_private=False)
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_reply(reply.text, reply.message.id, message.author.id, reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply']['reply']['text'] == reply.text

    @pytest.mark.django_db()
    def test_marks_discussion_as_open(self, auth_client, discussion_factory, user_factory,
                                      message_factory, reply_factory):
        message_author = user_factory()
        reply_author = user_factory()
        discussion = discussion_factory(topic__is_private=False)
        message = message_factory(time=datetime.now(tz=pytz.UTC) - timedelta(minutes=31), discussion=discussion,
                                  author=message_author)
        discussion.mark_as_stale()
        discussion.save()
        reply = reply_factory.build(message=message, author=reply_author)

        mutation = MutationGenerator.create_reply(reply.text, reply.message.id, message.author.id, reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createReply']['reply']['text'] == reply.text
        assert response.json()['data']['createReply']['reply']['message']['discussion']['status'] == 'OPEN'
