import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryGroups:

    @pytest.mark.django_db
    def test_get_group(self, team_factory, client):
        team = team_factory()

        query = QueryGenerator.get_team(team.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['team']['id'] == str(team.id)

    @pytest.mark.django_db
    def test_get_groups(self, team_factory, client):
        team_factory()
        team_factory()

        query = QueryGenerator.get_teams()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['teams']) == 2
