import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryTeams:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, team_factory):
        team = team_factory()

        query = QueryGenerator.get_team(team.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['team']

    @pytest.mark.django_db
    def test_get_team(self, user_client, team_factory):
        team = team_factory(members=[user_client.user])

        query = QueryGenerator.get_team(team.name)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['team']['id'] == str(team.id)

    @pytest.mark.django_db
    def test_get_teams(self, user_client, team_factory):
        team_factory(members=[user_client.user])
        team_factory()

        query = QueryGenerator.get_teams()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len([team for team in response.json()['data']['teams'] if team]) == 1
