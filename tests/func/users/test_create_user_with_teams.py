import pytest
from django.core import mail

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserWithTeams:
    # TODO: Break out creating users as superuser vs anonymous user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, team_factory):
        team = team_factory()
        user = user_factory.build()

        mutation = MutationGenerator.create_user_with_teams(email=user.email, username=user.username,
                                                            team_ids=[team.id])
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserWithTeams'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, superuser_client, user_factory, team_factory):
        assert not mail.outbox
        team = team_factory()
        user = user_factory.build()

        mutation = MutationGenerator.create_user_with_teams(email=user.email, username=user.username,
                                                            team_ids=[team.id + 1])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserWithTeams']
        assert response.json()['errors'][0]['message'] == str({'team_ids': [f'Invalid pk "{team.id + 1}" '
                                                                            f'- object does not exist.']})
        assert not mail.outbox

    @pytest.mark.django_db
    def test_valid(self, superuser_client, user_factory, team_factory):
        assert not mail.outbox
        team = team_factory()
        user = user_factory.build()

        mutation = MutationGenerator.create_user_with_teams(email=user.email, username=user.username,
                                                            team_ids=[team.id])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserWithTeams']['user']['email']
        assert response.json()['data']['createUserWithTeams']['user']['teams'][0]['name'] == team.name
        assert mail.outbox[0].subject == 'Welcome to Strand'
        assert mail.outbox[0].to == [user.email]
        assert mail.outbox[0].body
