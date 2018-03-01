import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserAndReplyFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, reply_factory, slack_event_factory,
                             slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message = message_factory(discussion=slack_channel.discussion)
        message_event = slack_event_factory(message=message)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, message_factory, reply_factory,
                                slack_event_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message = message_factory(discussion=slack_channel.discussion)
        message_event = slack_event_factory(message=message)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, message_factory, reply_factory,
                                slack_event_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message = message_factory(discussion=slack_channel.discussion)
        message_event = slack_event_factory(message=message)
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, message_factory, reply_factory,
                                   slack_event_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory.build()
        message = message_factory()
        message_event = slack_event_factory(message=message)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_message(self, auth_client, message_factory, reply_factory, slack_event_factory,
                             slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message = message_factory.build(discussion=slack_channel.discussion)
        message_event = slack_event_factory.build()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, reply_factory, slack_event_factory,
                   slack_channel_factory, slack_user_factory, slack_team_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message = message_factory(discussion=slack_channel.discussion)
        message_event = slack_event_factory(message=message)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_event = slack_event_factory.build()
        reply = reply_factory.build(message=message)

        mutation = MutationGenerator.create_user_and_reply_from_slack(id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_user.slack_team.id,
                                                                      message_origin_slack_event_ts=message_event.ts,
                                                                      origin_slack_event_ts=reply_event.ts,
                                                                      slack_channel_id=slack_channel.id,
                                                                      text=reply.text)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReplyFromSlack']['slackUser']['id'] == slack_user.id
        assert response.json()['data']['createUserAndReplyFromSlack']['user']['alias']
        assert response.json()['data']['createUserAndReplyFromSlack']['reply']['message']['id'] == str(message.id)
