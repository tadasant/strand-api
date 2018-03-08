import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestMarkDiscussionAsPendingClosedFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False, discussion__status='STALE')

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, discussion_factory, slack_channel_factory):
        discussion = discussion_factory(topic__is_private=False, status='STALE')
        slack_channel = slack_channel_factory.build(discussion=discussion)

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_discussion_state(self, auth_client, slack_channel_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False, discussion__status='OPEN')

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'OPEN' using method " \
                                                          "'mark_as_pending_closed'"

    @pytest.mark.django_db
    @pytest.mark.usefixtures('slack_app_request')
    def test_valid(self, auth_client, slack_channel_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False, discussion__status='STALE')

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack']['discussion'][
                   'status'] == 'PENDING CLOSED'
