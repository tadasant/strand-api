import pytest


class TestCreateDiscussionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, slack_channel_factory, slack_team_factory,
                             discussion_factory, topic_factory):
        topic = topic_factory(is_private=False)
        slack_team = slack_team_factory()
        discussion = discussion_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_discussion_from_slack(discussion.time_start, topic.id, slack_channel.id,
                                                                   slack_channel.name, slack_team.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, slack_channel_factory, slack_team_factory, discussion_factory,
                   topic_factory):
        topic = topic_factory(is_private=False)
        slack_team = slack_team_factory()
        discussion = discussion_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_discussion_from_slack(discussion.time_start, topic.id, slack_channel.id,
                                                                   slack_channel.name, slack_team.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussionFromSlack']['discussion']['topic']['id'] == str(topic.id)
        assert response.json()['data']['createDiscussionFromSlack']['slackChannel']['name'] == slack_channel.name
