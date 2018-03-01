import pytest


class TestCreateTopic:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build(is_private=False)

        mutation = mutation_generator.create_topic(title=topic.title, description=topic.description,
                                                   is_private=str(topic.is_private).lower(), original_poster_id=user.id,
                                                   group_id=group.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopic'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build(is_private=False)

        mutation = mutation_generator.create_topic(title=topic.title, description=topic.description,
                                                   is_private=str(topic.is_private).lower(), original_poster_id=user.id,
                                                   group_id=group.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopic']['topic']['title'] == topic.title

    @pytest.mark.django_db
    def test_valid_and_create_tags(self, auth_client, mutation_generator, topic_factory, user_factory, group_factory,
                                   tag_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build(is_private=False)
        tag_one = tag_factory.build()
        tag_two = tag_factory.build()

        mutation = mutation_generator.create_topic(title=topic.title, description=topic.description,
                                                   is_private=str(topic.is_private).lower(), original_poster_id=user.id,
                                                   group_id=group.id, tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopic']['topic']
        assert len(response.json()['data']['createTopic']['topic']['tags']) == 2
