import pytest


class TestQuerySlackChannels:

    @pytest.mark.django_db
    def test_get_slack_channel(self, client, query_generator, slack_channel_factory):
        slack_channel = slack_channel_factory()

        query = query_generator.get_slack_channel(slack_channel.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['slackChannel']['name'] == slack_channel.name

    @pytest.mark.django_db
    def test_get_slack_channels(self, client, query_generator, slack_channel_factory):
        slack_channel_factory()
        slack_channel_factory()

        query = query_generator.get_slack_channels()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['slackChannels']) == 2
