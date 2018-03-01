import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryMessages:

    @pytest.mark.django_db
    def test_get_message(self, client, message_factory):
        message = message_factory(discussion__topic__is_private=False)

        response = client.post('/graphql', {'query': QueryGenerator.get_message(message.id)})

        assert response.status_code == 200, response.content
        assert response.json()['data']['message']['text'] == message.text

    @pytest.mark.django_db
    def test_get_message_private_discussion_topic(self, client, message_factory):
        message = message_factory(discussion__topic__is_private=True)

        response = client.post('/graphql', {'query': QueryGenerator.get_message(message.id)})

        assert response.status_code == 200, response.content
        assert response.json()['data']['message'] is None

    @pytest.mark.django_db
    def test_get_messages(self, client, message_factory):
        message_factory(discussion__topic__is_private=False)
        message_factory(discussion__topic__is_private=False)

        response = client.post('/graphql', {'query': QueryGenerator.get_messages()})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['messages']) == 2
        assert response.json()['data']['messages'][0]['text']

    @pytest.mark.django_db
    def test_get_messages_private_discussion_topic(self, client, message_factory):
        message_factory(discussion__topic__is_private=True)
        message_factory(discussion__topic__is_private=True)

        response = client.post('/graphql', {'query': QueryGenerator.get_messages()})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['messages']) == 2
        assert response.json()['data']['messages'][0] is None
