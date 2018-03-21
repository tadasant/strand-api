import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateTeam:
    # TODO: Break out creating teams as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, team_factory):
        team = team_factory.build()

        mutation = MutationGenerator.create_team(team.name)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTeam'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, superuser_client, team_factory):
        team = team_factory.build()

        mutation = MutationGenerator.create_team(team.name)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTeam']['team']['name'] == team.name
