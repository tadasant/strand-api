import pytest


class TestQueryReplies:

    @pytest.mark.django_db
    def test_get_reply(self, reply_factory, client):
        reply = reply_factory(message__discussion__topic__is_private=False)

        query = {'query': f'{{ reply(id: {reply.id}) {{ message {{ text }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['reply']['message']['text']

    @pytest.mark.django_db
    def test_get_reply_private_discussion_topic(self, reply_factory, client):
        reply = reply_factory(message__discussion__topic__is_private=True)

        query = {'query': f'{{ reply(id: {reply.id}) {{ message {{ text }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['reply'] is None

    @pytest.mark.django_db
    def test_get_replies(self, reply_factory, client):
        reply_factory(message__discussion__topic__is_private=False)
        reply_factory(message__discussion__topic__is_private=False)

        query = {'query': '{ replies { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2
        assert response.json()['data']['replies'][0]['text']

    @pytest.mark.django_db
    def test_get_replies_private_discussion_topic(self, reply_factory, client):
        reply_factory(message__discussion__topic__is_private=True)
        reply_factory(message__discussion__topic__is_private=True)

        query = {'query': '{ replies { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2
        assert response.json()['data']['replies'][0] is None
