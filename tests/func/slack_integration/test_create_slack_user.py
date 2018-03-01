import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateSlackUser:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = MutationGenerator.create_slack_user(id=slack_user.id, name=slack_user.name,
                                                       real_name=slack_user.real_name,
                                                       display_name=slack_user.display_name,
                                                       image_72=slack_user.image_72,
                                                       is_bot=str(slack_user.is_bot).lower(),
                                                       is_admin=str(slack_user.is_admin).lower(),
                                                       slack_team_id=slack_team.id, user_id=user.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory.build()

        mutation = MutationGenerator.create_slack_user(id=slack_user.id, name=slack_user.name,
                                                       real_name=slack_user.real_name,
                                                       display_name=slack_user.display_name,
                                                       image_72=slack_user.image_72,
                                                       is_bot=str(slack_user.is_bot).lower(),
                                                       is_admin=str(slack_user.is_admin).lower(),
                                                       slack_team_id=slack_team.id, user_id=user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = MutationGenerator.create_slack_user(id=slack_user.id, name=slack_user.name,
                                                       real_name=slack_user.real_name,
                                                       display_name=slack_user.display_name,
                                                       image_72=slack_user.image_72,
                                                       is_bot=str(slack_user.is_bot).lower(),
                                                       is_admin=str(slack_user.is_admin).lower(),
                                                       slack_team_id=slack_team.id, user_id=1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['errors'][0]['message'] == "{'user_id': ['Invalid pk \"1\" - object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = MutationGenerator.create_slack_user(id=slack_user.id, name=slack_user.name,
                                                       real_name=slack_user.real_name,
                                                       display_name=slack_user.display_name,
                                                       image_72=slack_user.image_72,
                                                       is_bot=str(slack_user.is_bot).lower(),
                                                       is_admin=str(slack_user.is_admin).lower(),
                                                       slack_team_id=slack_team.id, user_id=user.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createSlackUser']['slackUser']['id'] == slack_user.id
