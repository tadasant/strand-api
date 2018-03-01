import pytest


class TestCreateUserFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)

        mutation = mutation_generator.create_user_from_slack(id=slack_user.id, name=slack_user.name,
                                                             first_name=slack_user.first_name,
                                                             last_name=slack_user.last_name,
                                                             real_name=slack_user.real_name,
                                                             display_name=slack_user.display_name,
                                                             email=slack_user.email,
                                                             image_72=slack_user.image_72,
                                                             is_bot=str(slack_user.is_bot).lower(),
                                                             is_admin=str(slack_user.is_admin).lower(),
                                                             slack_team_id=slack_team.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_existing_slack_user(self, auth_client, mutation_generator, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory(slack_team=slack_team)

        mutation = mutation_generator.create_user_from_slack(id=slack_user.id, name=slack_user.name,
                                                             first_name=slack_user.first_name,
                                                             last_name=slack_user.last_name,
                                                             real_name=slack_user.real_name,
                                                             display_name=slack_user.display_name,
                                                             email=slack_user.email,
                                                             image_72=slack_user.image_72,
                                                             is_bot=str(slack_user.is_bot).lower(),
                                                             is_admin=str(slack_user.is_admin).lower(),
                                                             slack_team_id=slack_team.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_valid_and_gets_user(self, auth_client, mutation_generator, slack_team_factory, user_factory,
                                 slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = mutation_generator.create_user_from_slack(id=slack_user.id, name=slack_user.name,
                                                             first_name=slack_user.first_name,
                                                             last_name=slack_user.last_name,
                                                             real_name=slack_user.real_name,
                                                             display_name=slack_user.display_name,
                                                             email=slack_user.email,
                                                             image_72=slack_user.image_72,
                                                             is_bot=str(slack_user.is_bot).lower(),
                                                             is_admin=str(slack_user.is_admin).lower(),
                                                             slack_team_id=slack_team.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack']['slackUser']['user']['id'] == str(user.id)

    @pytest.mark.django_db
    def test_valid_and_creates_user(self, auth_client, mutation_generator, slack_team_factory, user_factory,
                                    slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = mutation_generator.create_user_from_slack(id=slack_user.id, name=slack_user.name,
                                                             first_name=slack_user.first_name,
                                                             last_name=slack_user.last_name,
                                                             real_name=slack_user.real_name,
                                                             display_name=slack_user.display_name,
                                                             email=slack_user.email,
                                                             image_72=slack_user.image_72,
                                                             is_bot=str(slack_user.is_bot).lower(),
                                                             is_admin=str(slack_user.is_admin).lower(),
                                                             slack_team_id=slack_team.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack']['slackUser']['user']['alias']
