import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQuerySlackChannels:

    @pytest.mark.django_db
    def test_get_slack_channel(self, client, slack_channel_factory):
        slack_channel = slack_channel_factory()

        query = QueryGenerator.get_slack_channel(slack_channel.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['slackChannel']['name'] == slack_channel.name

    @pytest.mark.django_db
    def test_get_slack_channels(self, client, slack_channel_factory):
        slack_channel_factory()
        slack_channel_factory()

        query = QueryGenerator.get_slack_channels()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['slackChannels']) == 2
