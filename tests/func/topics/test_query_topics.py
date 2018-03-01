import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryTopics:

    @pytest.mark.django_db
    def test_get_topic(self, client, topic_factory):
        topic = topic_factory(is_private=False)

        query = QueryGenerator.get_topic(topic.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['topic']['title'] == topic.title

    @pytest.mark.django_db
    def test_get_private_topic(self, client, topic_factory):
        topic = topic_factory(is_private=True)

        query = QueryGenerator.get_topic(topic.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['topic'] is None

    @pytest.mark.django_db
    def test_get_topics(self, client, topic_factory):
        topic_factory(is_private=False)
        topic_factory(is_private=False)

        query = QueryGenerator.get_topics()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['topics']) == 2
        assert response.json()['data']['topics'][0]

    @pytest.mark.django_db
    def test_get_private_topics(self, client, topic_factory):
        topic_factory(is_private=True)
        topic_factory(is_private=True)

        query = QueryGenerator.get_topics()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['topics']) == 2
        assert response.json()['data']['topics'][0] is None
