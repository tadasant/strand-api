import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCloseDiscussionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory, slack_channel_factory, slack_user_factory):
        discussion = discussion_factory(topic__is_private=False)
        slack_user = slack_user_factory(is_admin=True)
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = MutationGenerator.close_discussion_from_slack(slack_channel.id, slack_user.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, discussion_factory, slack_channel_factory, slack_user_factory):
        discussion = discussion_factory(topic__is_private=False)
        slack_user = slack_user_factory(is_admin=True)
        slack_channel = slack_channel_factory.build(discussion=discussion)

        mutation = MutationGenerator.close_discussion_from_slack(slack_channel.id, slack_user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, discussion_factory, slack_channel_factory, slack_user_factory):
        slack_user = slack_user_factory(is_admin=False)
        discussion = discussion_factory(topic__is_private=False)
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = MutationGenerator.close_discussion_from_slack(slack_channel.id, slack_user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Slack user does not have permission to close discussion'

    @pytest.mark.django_db
    def test_valid_op(self, auth_client, discussion_factory, slack_channel_factory, slack_user_factory):
        slack_user = slack_user_factory()
        discussion = discussion_factory(topic__is_private=False, topic__original_poster=slack_user.user)
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = MutationGenerator.close_discussion_from_slack(slack_channel.id, slack_user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussionFromSlack']['discussion']['status'] == 'CLOSED'

    @pytest.mark.django_db
    def test_valid_admin(self, auth_client, discussion_factory, slack_channel_factory, slack_user_factory):
        discussion = discussion_factory(topic__is_private=False)
        slack_user = slack_user_factory(is_admin=True)
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = MutationGenerator.close_discussion_from_slack(slack_channel.id, slack_user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['closeDiscussionFromSlack']['discussion']['status'] == 'CLOSED'
