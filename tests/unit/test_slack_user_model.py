import pytest

from app.slack_integration.models import SlackUser
from app.users.models import User


class TestSlackUserModel:

    @pytest.mark.django_db
    def test_display_name_is_null(self, slack_user_factory, slack_team_factory):
        """
        Given: The database has been created.
        When: A user is created without an email.
        Then: No constraint is violated.
        """
        slack_team = slack_team_factory()
        slack_user_data = slack_user_factory.build()

        slack_user = SlackUser(id=slack_user_data.id, name=slack_user_data.name, first_name='', last_name='',
                               real_name=slack_user_data.real_name, display_name=None,
                               email=slack_user_data.email, image_72=slack_user_data.image_72,
                               is_bot=slack_user_data.is_bot, is_admin=slack_user_data.is_admin,
                               slack_team=slack_team)

        try:
            user = User.objects.get(email=slack_user.email)
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            User.objects.create_user_from_slack_user(slack_user)

        assert SlackUser.objects.filter(id=slack_user.id).exists()
