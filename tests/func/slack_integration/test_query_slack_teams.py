import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQuerySlackTeams:

    @pytest.mark.django_db
    def test_get_slack_team(self, client, slack_team_factory):
        slack_team = slack_team_factory()

        query = QueryGenerator.get_slack_team(slack_team.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['slackTeam']['name'] == slack_team.name

    @pytest.mark.django_db
    def test_get_slack_teams(self, client, slack_team_factory):
        slack_team_factory()
        slack_team_factory()

        query = QueryGenerator.get_slack_teams()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['slackTeams']) == 2
