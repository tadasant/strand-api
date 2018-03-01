import pytest


class TestCloseDiscussion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = mutation_generator.close_discussion(discussion_id=discussion.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, mutation_generator, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = mutation_generator.close_discussion(discussion_id=discussion.id + 1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = mutation_generator.close_discussion(discussion_id=discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion']['discussion']['id'] == str(discussion.id)
