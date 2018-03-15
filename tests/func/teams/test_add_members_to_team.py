import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestAddMembersToTeam:
    # TODO: Break out creating teams as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, team_factory, user_factory):
        team = team_factory()
        jimmy = user_factory()

        mutation = MutationGenerator.add_members_to_team(id=team.id, member_ids=[jimmy.id])
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['addMembersToTeam']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_user(self, superuser_client, team_factory, user_factory):
        team = team_factory()
        jimmy = user_factory()

        mutation = MutationGenerator.add_members_to_team(id=team.id, member_ids=[jimmy.id + 1])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['addMembersToTeam']
        assert response.json()['errors'][0]['message'] == str({'member_ids': [f'Invalid pk "{jimmy.id + 1}" '
                                                                              f'- object does not exist.']})

    @pytest.mark.django_db
    def test_valid(self, superuser_client, team_factory, user_factory):
        team = team_factory(members=[user_factory()])
        jimmy = user_factory()

        mutation = MutationGenerator.add_members_to_team(id=team.id, member_ids=[jimmy.id])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['addMembersToTeam']['team']['members'][1]['email'] == jimmy.email
