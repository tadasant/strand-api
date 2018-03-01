import pytest


class TestCreateUserAndMessageFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, message_factory, slack_event_factory, slack_user_factory,
                             slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        mutation = mutation_generator.create_user_and_message_from_slack(id=slack_user.id, name=slack_user.name,
                                                                         first_name=slack_user.first_name,
                                                                         last_name=slack_user.last_name,
                                                                         real_name=slack_user.real_name,
                                                                         display_name=slack_user.display_name,
                                                                         email=slack_user.email,
                                                                         image_72=slack_user.image_72,
                                                                         is_bot=str(slack_user.is_bot).lower(),
                                                                         is_admin=str(slack_user.is_admin).lower(),
                                                                         slack_team_id=slack_user.slack_team_id,
                                                                         origin_slack_event_ts=slack_event.ts,
                                                                         slack_channel_id=slack_channel.id,
                                                                         text=message.text)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, mutation_generator, message_factory, slack_event_factory,
                                slack_user_factory, slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        mutation = mutation_generator.create_user_and_message_from_slack(id=slack_user.id, name=slack_user.name,
                                                                         first_name=slack_user.first_name,
                                                                         last_name=slack_user.last_name,
                                                                         real_name=slack_user.real_name,
                                                                         display_name=slack_user.display_name,
                                                                         email=slack_user.email,
                                                                         image_72=slack_user.image_72,
                                                                         is_bot=str(slack_user.is_bot).lower(),
                                                                         is_admin=str(slack_user.is_admin).lower(),
                                                                         slack_team_id=slack_user.slack_team_id,
                                                                         origin_slack_event_ts=slack_event.ts,
                                                                         slack_channel_id=slack_channel.id,
                                                                         text=message.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, mutation_generator, message_factory, slack_event_factory,
                                slack_user_factory, slack_channel_factory):
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build()
        message = message_factory.build()
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        mutation = mutation_generator.create_user_and_message_from_slack(id=slack_user.id, name=slack_user.name,
                                                                         first_name=slack_user.first_name,
                                                                         last_name=slack_user.last_name,
                                                                         real_name=slack_user.real_name,
                                                                         display_name=slack_user.display_name,
                                                                         email=slack_user.email,
                                                                         image_72=slack_user.image_72,
                                                                         is_bot=str(slack_user.is_bot).lower(),
                                                                         is_admin=str(slack_user.is_admin).lower(),
                                                                         slack_team_id=slack_user.slack_team_id,
                                                                         origin_slack_event_ts=slack_event.ts,
                                                                         slack_channel_id=slack_channel.id,
                                                                         text=message.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk " \
                                                          f"\"{slack_user.slack_team_id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, mutation_generator, message_factory, slack_event_factory,
                                   slack_user_factory, slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_user_and_message_from_slack(id=slack_user.id, name=slack_user.name,
                                                                         first_name=slack_user.first_name,
                                                                         last_name=slack_user.last_name,
                                                                         real_name=slack_user.real_name,
                                                                         display_name=slack_user.display_name,
                                                                         email=slack_user.email,
                                                                         image_72=slack_user.image_72,
                                                                         is_bot=str(slack_user.is_bot).lower(),
                                                                         is_admin=str(slack_user.is_admin).lower(),
                                                                         slack_team_id=slack_user.slack_team_id,
                                                                         origin_slack_event_ts=slack_event.ts,
                                                                         slack_channel_id=slack_channel.id,
                                                                         text=message.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, message_factory, slack_event_factory, slack_user_factory,
                   slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        mutation = mutation_generator.create_user_and_message_from_slack(id=slack_user.id, name=slack_user.name,
                                                                         first_name=slack_user.first_name,
                                                                         last_name=slack_user.last_name,
                                                                         real_name=slack_user.real_name,
                                                                         display_name=slack_user.display_name,
                                                                         email=slack_user.email,
                                                                         image_72=slack_user.image_72,
                                                                         is_bot=str(slack_user.is_bot).lower(),
                                                                         is_admin=str(slack_user.is_admin).lower(),
                                                                         slack_team_id=slack_user.slack_team_id,
                                                                         origin_slack_event_ts=slack_event.ts,
                                                                         slack_channel_id=slack_channel.id,
                                                                         text=message.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack']['slackUser']['user']['alias']
