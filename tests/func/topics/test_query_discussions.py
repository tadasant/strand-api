import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryDiscussions:

    @pytest.mark.django_db
    def test_get_discussion(self, client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        query = QueryGenerator.get_discussion(discussion.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['discussion']['topic']['title'] == discussion.topic.title

    @pytest.mark.django_db
    def test_get_discussion_private_topic(self, client, discussion_factory):
        discussion = discussion_factory(topic__is_private=True)

        query = QueryGenerator.get_discussion(discussion.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['discussion'] is None

    @pytest.mark.django_db
    def test_get_discussions(self, client, discussion_factory):
        discussion_factory(topic__is_private=False)
        discussion_factory(topic__is_private=False)

        query = QueryGenerator.get_discussions()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['discussions']) == 2
        assert response.json()['data']['discussions'][0]

    @pytest.mark.django_db
    def test_get_discussions_private_topic(self, client, discussion_factory):
        discussion_factory(topic__is_private=True)
        discussion_factory(topic__is_private=True)

        query = QueryGenerator.get_discussions()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['discussions']) == 2
        assert response.json()['data']['discussions'][0] is None
