import pytest


class TestQuerySlackTeams:

    @pytest.mark.django_db
    def test_get_slack_team(self, client, query_generator, slack_team_factory):
        slack_team = slack_team_factory()

        query = query_generator.get_slack_team(slack_team.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['slackTeam']['name'] == slack_team.name

    @pytest.mark.django_db
    def test_get_slack_teams(self, client, query_generator, slack_team_factory):
        slack_team_factory()
        slack_team_factory()

        query = query_generator.get_slack_teams()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['slackTeams']) == 2
