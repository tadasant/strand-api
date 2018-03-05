import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCloseDiscussion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = MutationGenerator.close_discussion(discussion_id=discussion.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = MutationGenerator.close_discussion(discussion_id=discussion.id + 1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False)

        mutation = MutationGenerator.close_discussion(discussion_id=discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussion']['discussion']['id'] == str(discussion.id)
