import pytest


class TestQueryMessages:

    @pytest.mark.django_db
    def test_get_message(self, message_factory, client):
        message = message_factory(discussion__topic__is_private=False)

        query = {'query': f'{{ message(id: {message.id}) {{ text }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['message']['text'] == message.text

    @pytest.mark.django_db
    def test_get_message_private_discussion_topic(self, message_factory, client):
        message = message_factory(discussion__topic__is_private=True)

        query = {'query': f'{{ message(id: {message.id}) {{ text }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['message'] is None

    @pytest.mark.django_db
    def test_get_messages(self, message_factory, client):
        message_factory(discussion__topic__is_private=False)
        message_factory(discussion__topic__is_private=False)

        query = {'query': '{ messages { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['messages']) == 2
        assert response.json()['data']['messages'][0]['text']

    @pytest.mark.django_db
    def test_get_messages_private_discussion_topic(self, message_factory, client):
        message_factory(discussion__topic__is_private=True)
        message_factory(discussion__topic__is_private=True)

        query = {'query': '{ messages { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['messages']) == 2
        assert response.json()['data']['messages'][0] is None
