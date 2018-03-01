import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestMarkDiscussionAsPendingClosed:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')

        mutation = MutationGenerator.mark_discussion_as_pending_closed(discussion.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosed'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client):
        mutation = MutationGenerator.mark_discussion_as_pending_closed(1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosed'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_discussion_state(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='OPEN')

        mutation = MutationGenerator.mark_discussion_as_pending_closed(discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosed'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'OPEN' using method " \
                                                          "'mark_as_pending_closed'"

    @pytest.mark.django_db
    @pytest.mark.usefixtures('auto_close_pending_closed_discussion_task', 'slack_app_request')
    def test_valid(self, auth_client, discussion_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')

        mutation = MutationGenerator.mark_discussion_as_pending_closed(discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosed']['discussion'][
                   'status'] == 'PENDING CLOSED'
