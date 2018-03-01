import pytest


class TestQueryReplies:

    @pytest.mark.django_db
    def test_get_reply(self, client, query_generator, reply_factory):
        reply = reply_factory(message__discussion__topic__is_private=False)

        response = client.post('/graphql', {'query': query_generator.get_reply(reply.id)})

        assert response.status_code == 200
        assert response.json()['data']['reply']['message']['text']

    @pytest.mark.django_db
    def test_get_reply_private_discussion_topic(self, client, query_generator, reply_factory):
        reply = reply_factory(message__discussion__topic__is_private=True)

        response = client.post('/graphql', {'query': query_generator.get_reply(reply.id)})

        assert response.status_code == 200
        assert response.json()['data']['reply'] is None

    @pytest.mark.django_db
    def test_get_replies(self, client, query_generator, reply_factory):
        reply_factory(message__discussion__topic__is_private=False)
        reply_factory(message__discussion__topic__is_private=False)

        response = client.post('/graphql', {'query': query_generator.get_replies()})

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2
        assert response.json()['data']['replies'][0]['text']

    @pytest.mark.django_db
    def test_get_replies_private_discussion_topic(self, client, query_generator, reply_factory):
        reply_factory(message__discussion__topic__is_private=True)
        reply_factory(message__discussion__topic__is_private=True)

        response = client.post('/graphql', {'query': query_generator.get_replies()})

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2
        assert response.json()['data']['replies'][0] is None
