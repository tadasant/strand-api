import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateMessageFromSlack:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, user_factory, slack_user_factory,
                             slack_event_factory, message_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, slack_channel_factory, user_factory,
                                slack_user_factory, slack_event_factory, message_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        user = user_factory()
        slack_user = slack_user_factory.build(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, slack_channel_factory, user_factory,
                                   slack_user_factory, slack_event_factory, message_factory):
        slack_channel = slack_channel_factory.build()
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory, slack_channel_factory, user_factory,
                   slack_user_factory, slack_event_factory, message_factory):
        discussion = discussion_factory(topic__is_private=False)
        slack_channel = slack_channel_factory(discussion=discussion)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createMessageFromSlack']['message']['author']['id'] == \
            str(slack_user.user.id)
        assert response.json()['data']['createMessageFromSlack']['message']['discussion']['id'] == str(discussion.id)
        assert {'id': str(user.id)} in response.json()['data']['createMessageFromSlack']['message']['discussion'][
            'participants']
