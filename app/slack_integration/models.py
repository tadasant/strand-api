from enum import Enum

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from app.dialogues.models import Message
from app.groups.models import Group
from app.api.wrappers import SlackAppClientWrapper
from app.topics.models import Discussion
from app.users.models import User


class SlackAgentStatus(Enum):
    INITIATED = 'INITIATED'
    AUTHENTICATED = 'AUTHENTICATED'
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    INACTIVE = 'INACTIVE'


class SlackAgent(TimeStampedModel):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='slack_agent', primary_key=True)
    status = FSMField(default=SlackAgentStatus.INITIATED.value, protected=True)
    topic_channel_id = models.CharField(max_length=255, blank=True, null=True)

    def get_or_create_slack_application_installation_from_oauth(self, oauth_info):
        slack_user = SlackUser.objects.get(id=oauth_info['user_id'])
        # TODO: The purpose of this is to overwrite slack application installations. In the future
        # we probably want to delete and create (this could be done by moving the FK to Slack Agent.
        installation, created = SlackApplicationInstallation.objects.get_or_create(slack_agent_id=self.pk,
                                                                                   defaults=dict(
                                                                                       access_token=oauth_info[
                                                                                           'access_token'],
                                                                                       scope=oauth_info['scope'],
                                                                                       installer=slack_user,
                                                                                       bot_user_id=oauth_info[
                                                                                           'bot']['bot_user_id'],
                                                                                       bot_access_token=oauth_info[
                                                                                           'bot']['bot_access_token']))
        if not created:
            installation.access_token = oauth_info['access_token']
            installation.scope = oauth_info['scope']
            installation.installer = slack_user
            installation.bot_user_id = oauth_info['bot']['bot_user_id']
            installation.bot_access_token = oauth_info['bot']['bot_access_token']
            installation.save()

        return installation

    @property
    def is_initiated(self):
        return self.status == SlackAgentStatus.INITIATED.value

    def can_authenticate(self):
        return bool(self.slack_application_installation)

    # TODO: We should sync with state of installed slack application. When we do this, we can only authenticate
    # from initiated and inactive.
    @transition(status, source='*', target=SlackAgentStatus.AUTHENTICATED.value, conditions=[can_authenticate])
    def authenticate(self):
        pass

    def can_activate(self):
        return bool(self.topic_channel_id)

    @transition(field=status, source=[SlackAgentStatus.AUTHENTICATED.value, SlackAgentStatus.PAUSED.value,
                                      SlackAgentStatus.INACTIVE.value, SlackAgentStatus.ACTIVE.value],
                target=SlackAgentStatus.ACTIVE.value,
                conditions=[can_activate])
    def activate(self):
        pass

    @transition(field=status, source=SlackAgentStatus.ACTIVE.value, target=SlackAgentStatus.PAUSED.value)
    def pause(self):
        pass

    @transition(field=status, source=[SlackAgentStatus.ACTIVE.value, SlackAgentStatus.PAUSED.value],
                target=SlackAgentStatus.INACTIVE)
    def inactivate(self):
        pass

    def __str__(self):
        return f'Slack Agent for {self.group.name}'


class SlackTeam(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_agent = models.OneToOneField(to=SlackAgent, on_delete=models.CASCADE, related_name='slack_team')

    def __str__(self):
        return self.name


class SlackUser(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    real_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True)
    image_72 = models.CharField(max_length=255)
    is_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE, related_name='slack_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slack_users')

    def can_close_discussion(self, discussion):
        return self.is_admin or discussion.topic.original_poster == self.user

    def __str__(self):
        return f'{self.real_name or self.name}'


class SlackApplicationInstallation(TimeStampedModel):
    slack_agent = models.OneToOneField(to=SlackAgent, on_delete=models.CASCADE,
                                       related_name='slack_application_installation')
    access_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    installer = models.OneToOneField(to=SlackUser, on_delete=models.CASCADE)
    bot_user_id = models.CharField(max_length=255)
    bot_access_token = models.CharField(max_length=255)

    def __str__(self):
        return f'Installation for {self.slack_agent.slack_team.name}'


class SlackChannel(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_team = models.ForeignKey(to=SlackTeam, on_delete=models.CASCADE, related_name='slack_channels')
    discussion = models.OneToOneField(to=Discussion, on_delete=models.CASCADE, null=True, related_name='slack_channel')

    def __str__(self):
        return f'#{self.name}'


class SlackEvent(TimeStampedModel):
    message = models.OneToOneField(to=Message, on_delete=models.CASCADE, related_name='slack_event')
    ts = models.CharField(max_length=255)


@receiver(pre_save, sender=SlackAgent)
def pre_save_slack_agent(sender, instance=None, update_fields=None, **kwargs):
    """Create or update Slack Agent on Slack App

    If this is triggered by changing the status of a Slack Agent from
    INITIATED to AUTHENTICATED, then the Slack Agent needs to be
    created on the Slack App. If this is triggered by some other
    attribute change, then the Slack Agent needs to be updated on the
    Slack App. If this triggered by creating a Slack Agent, then we
    do nothing.
    """
    try:
        slack_agent = SlackAgent.objects.get(pk=instance.pk)
    except SlackAgent.DoesNotExist:
        pass
    else:
        if instance.status == SlackAgentStatus.AUTHENTICATED.value and \
                slack_agent.status == SlackAgentStatus.INITIATED.value:
            SlackAppClientWrapper.post_slack_agent(instance)
        else:
            SlackAppClientWrapper.put_slack_agent(instance)
