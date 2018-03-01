import json
import pytz
from datetime import datetime, timedelta

import pytest
from django.conf import settings

from app.topics.models import Discussion
from tests.utils import wait_until
from tests.resources.MutationGenerator import MutationGenerator


class TestMarkingDiscussionAsStale:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixture('use_slack_domain')
    def test_does_become_stale_with_no_messages(self, mark_stale_discussion_task, discussion_factory,
                                                slack_app_request):
        mark_stale_discussion_task(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=5)

        assert Discussion.objects.get(pk=discussion.id).is_stale
        assert not slack_app_request.calls

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixture('use_slack_domain')
    def test_does_not_become_stale_with_non_bot_message(self, mark_stale_discussion_task, auth_client,
                                                        discussion_factory, slack_channel_factory,
                                                        message_factory, user_factory, slack_user_factory,
                                                        slack_event_factory, slack_app_request):
        mark_stale_discussion_task(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        user = user_factory(is_bot=False)
        slack_user = slack_user_factory(user=user)
        slack_event = slack_event_factory.build(ts=(original_time + timedelta(minutes=2)).timestamp())
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=5)

        assert not Discussion.objects.get(pk=discussion.id).is_stale
        assert not slack_app_request.calls

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixtures('use_slack_domain')
    def test_does_become_stale_with_bot_message(self, mark_stale_discussion_task, auth_client, discussion_factory,
                                                slack_channel_factory, message_factory,
                                                user_factory, slack_user_factory, slack_event_factory,
                                                slack_app_request):
        mark_stale_discussion_task(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=57)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        user = user_factory(is_bot=True)
        slack_user = slack_user_factory(user=user)
        slack_event = slack_event_factory.build(ts=(original_time + timedelta(minutes=2)).timestamp())
        message = message_factory.build()

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        wait_until(condition=lambda: len(slack_app_request.calls) == 1, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_stale
        assert discussion.slack_channel
        assert len(slack_app_request.calls) == 1
        assert slack_app_request.calls[0].request.url == settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT
        assert slack_app_request.calls[0].request.body == \
            json.dumps({'slack_channel_id': slack_channel.id, 'slack_team_id': slack_channel.slack_team.id}).encode()


class TestClosingPendingClosedDiscussion:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixtures('use_slack_domain', 'auto_close_pending_closed_discussion_task')
    def test_does_get_closed(self, auth_client, discussion_factory, slack_channel_factory,
                             message_factory, user_factory, slack_user_factory, slack_event_factory, slack_app_request):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)

        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)

        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=30)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=non_bot_slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        discussion.mark_as_stale()
        discussion.save()

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel_id=slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content
        assert not Discussion.objects.get(pk=discussion.id).is_closed

        wait_until(condition=lambda: len(slack_app_request.calls) == 1, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert len(slack_app_request.calls) == 1
        assert slack_app_request.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT
        assert slack_app_request.calls[0].request.body == \
            json.dumps({'slack_channel_id': slack_channel.id, 'slack_team_id': slack_channel.slack_team.id}).encode()

    @pytest.mark.django_db
    @pytest.mark.usefixtures('use_slack_domain', 'auto_close_pending_closed_discussion_task')
    def test_does_not_get_closed_with_non_bot_message(self, auth_client, discussion_factory,
                                                      slack_channel_factory, message_factory, user_factory,
                                                      slack_user_factory, slack_event_factory, slack_app_request):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        # Old message sent
        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=non_bot_slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        # Discussion marked as stale
        discussion.mark_as_stale()
        discussion.save()

        # Discussion marked as pending closed
        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel_id=slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content
        assert not Discussion.objects.get(pk=discussion.id).is_closed

        # New message sent
        slack_event = slack_event_factory(ts=datetime.utcnow().timestamp())
        message = message_factory.build(discussion=discussion, author=non_bot_user)

        mutation = MutationGenerator.create_message_from_slack(text=message.text,
                                                               slack_channel_id=slack_channel.id,
                                                               slack_user_id=non_bot_slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_closed, timeout=5)

        assert not Discussion.objects.get(pk=discussion.id).is_closed
        assert not slack_app_request.calls

    @pytest.mark.django_db
    @pytest.mark.usefixtures('use_slack_domain', 'auto_close_pending_closed_discussion_task')
    def test_does_get_closed_with_bot_message(self, auth_client, discussion_factory,
                                              slack_channel_factory, message_factory, user_factory, slack_user_factory,
                                              slack_event_factory, slack_app_request):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        bot_user = user_factory(is_bot=True)
        bot_slack_user = slack_user_factory(user=bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        # Old message sent
        mutation = MutationGenerator.create_message_from_slack(text=message.text, slack_channel_id=slack_channel.id,
                                                               slack_user_id=non_bot_slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        # Discussion marked as stale
        discussion.mark_as_stale()
        discussion.save()

        # Discussion marked as pending closed
        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel_id=slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content
        assert not Discussion.objects.get(pk=discussion.id).is_closed
        assert not slack_app_request.calls

        # New message sent
        slack_event = slack_event_factory(ts=datetime.now(pytz.UTC).timestamp())
        message = message_factory.build(discussion=discussion, author=bot_user)

        mutation = MutationGenerator.create_message_from_slack(text=message.text, slack_channel_id=slack_channel.id,
                                                               slack_user_id=bot_slack_user.id,
                                                               origin_slack_event_ts=slack_event.ts)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        wait_until(condition=lambda: len(slack_app_request.calls) == 1, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert discussion.slack_channel
        assert len(slack_app_request.calls) == 1
        assert slack_app_request.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT
        assert slack_app_request.calls[0].request.body == \
            json.dumps({'slack_channel_id': slack_channel.id, 'slack_team_id': slack_channel.slack_team.id}).encode()

    @pytest.mark.django_db
    @pytest.mark.usefixtures('use_slack_domain', 'auto_close_pending_closed_discussion_task')
    def test_does_get_closed_with_no_messages_ever(self, auth_client, discussion_factory,
                                                   slack_channel_factory, slack_app_request):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(topic__is_private=False, time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)

        discussion.mark_as_stale()
        discussion.save()

        mutation = MutationGenerator.mark_discussion_as_pending_closed_from_slack(slack_channel_id=slack_channel.id)
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200, response.content

        wait_until(condition=lambda: len(slack_app_request.calls) == 1, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert len(slack_app_request.calls) == 1
        assert slack_app_request.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT
        assert slack_app_request.calls[0].request.body == \
            json.dumps({'slack_channel_id': slack_channel.id, 'slack_team_id': slack_channel.slack_team.id}).encode()
