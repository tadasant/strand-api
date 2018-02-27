import pytest


class TestQueryDiscussions:

    @pytest.mark.django_db
    def test_get_discussion(self, discussion_factory, client):
        discussion = discussion_factory(topic__is_private=False)

        query = {'query': f'{{ discussion(id: {discussion.id}) {{ topic {{ title }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['discussion']['topic']['title'] == discussion.topic.title

    @pytest.mark.django_db
    def test_get_discussion_private_topic(self, discussion_factory, client):
        discussion = discussion_factory(topic__is_private=True)

        query = {'query': f'{{ discussion(id: {discussion.id}) {{ topic {{ title }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['discussion'] is None

    @pytest.mark.django_db
    def test_get_discussions(self, discussion_factory, client):
        discussion_factory(topic__is_private=False)
        discussion_factory(topic__is_private=False)

        query = {'query': '{ discussions { id } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['discussions']) == 2
        assert response.json()['data']['discussions'][0]

    @pytest.mark.django_db
    def test_get_discussions_private_topic(self, discussion_factory, client):
        discussion_factory(topic__is_private=True)
        discussion_factory(topic__is_private=True)

        query = {'query': '{ discussions { id } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['discussions']) == 2
        assert response.json()['data']['discussions'][0] is None
