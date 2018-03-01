import pytest


class TestQueryTopics:

    @pytest.mark.django_db
    def test_get_topic(self, client, query_generator, topic_factory):
        topic = topic_factory(is_private=False)

        query = query_generator.get_topic(topic.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['topic']['title'] == topic.title

    @pytest.mark.django_db
    def test_get_private_topic(self, client, query_generator, topic_factory):
        topic = topic_factory(is_private=True)

        query = query_generator.get_topic(topic.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['topic'] is None

    @pytest.mark.django_db
    def test_get_topics(self, client, query_generator, topic_factory):
        topic_factory(is_private=False)
        topic_factory(is_private=False)

        query = query_generator.get_topics()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['topics']) == 2
        assert response.json()['data']['topics'][0]

    @pytest.mark.django_db
    def test_get_private_topics(self, client, query_generator, topic_factory):
        topic_factory(is_private=True)
        topic_factory(is_private=True)

        query = query_generator.get_topics()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['topics']) == 2
        assert response.json()['data']['topics'][0] is None
