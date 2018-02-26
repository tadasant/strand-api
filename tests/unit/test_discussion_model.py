import pytz
from datetime import datetime, timedelta

import pytest


class TestDiscussionModel:

    @pytest.mark.django_db
    def test_minutes_since_last_non_bot_message(self, user_factory, message_factory, discussion_factory):
        """
        Given: A discussion's last non-bot message is over a day old.
        When: The minutes_since_last_non_bot_message is computed.
        Then: The minutes > 1440.
        """
        discussion = discussion_factory()
        user = user_factory(is_bot=False)
        message_time = datetime.now(tz=pytz.UTC) - timedelta(days=1, minutes=30)
        message_factory(author=user, time=message_time, discussion=discussion)

        assert discussion.minutes_since_last_non_bot_message >= ((60 * 24) + 30)
