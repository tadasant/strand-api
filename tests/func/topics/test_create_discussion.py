import pytest


class TestCreateDiscussion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, topic_factory, discussion_factory):
        topic = topic_factory(is_private=False)
        discussion = discussion_factory.build()

        mutation = mutation_generator.create_discussion(time_start=discussion.time_start,
                                                        time_end=discussion.time_end,
                                                        topic_id=topic.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, topic_factory, discussion_factory):
        topic = topic_factory(is_private=False)
        discussion = discussion_factory.build()

        mutation = mutation_generator.create_discussion(time_start=discussion.time_start,
                                                        time_end=discussion.time_end,
                                                        topic_id=topic.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussion']['discussion']['topic']['id'] == str(topic.id)
