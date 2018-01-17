import graphene

from app.groups.models import Group
from app.groups.types import GroupType
from app.messages.models import Message, Reply
from app.messages.types import MessageType, ReplyType
from app.questions.models import Question, Session
from app.questions.types import SessionType, QuestionType
from app.slack.models import (
    SlackChannel,
    SlackEvent,
    SlackTeamSetting,
    SlackTeamInstallation,
    SlackTeam,
    SlackUser
)
from app.slack.types import (
    GroupFromSlackInputType,
    MessageFromSlackInputType,
    ReplyFromSlackInputType,
    SessionFromSlackInputType,
    SlackChannelType,
    SlackChannelInputType,
    SlackEventType,
    SlackTeamSettingType,
    SlackTeamSettingInputType,
    SlackTeamType,
    SlackTeamInputType,
    SlackTeamInstallationType,
    SlackTeamInstallationInputType,
    SlackUserType,
    SlackUserInputType,
    SolveQuestionFromSlackInputType,
    UserFromSlackInputType
)
from app.users.models import User
from app.users.types import UserType


class CreateSlackUserMutation(graphene.Mutation):
    class Arguments:
        input = SlackUserInputType(required=True)

    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        if not User.objects.filter(pk=input.user_id).exists():
            raise Exception('Invalid User Id')

        slack_user = SlackUser.objects.create(**input)

        return CreateSlackUserMutation(slack_user=slack_user)


class CreateSlackTeamMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInputType(required=True)

    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Group.objects.filter(pk=input.group_id).exists():
            raise Exception('Invalid Group Id')

        slack_team = SlackTeam.objects.create(**input)

        return CreateSlackTeamMutation(slack_team=slack_team)


class CreateSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SlackChannelInputType(required=True)

    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        if not Session.objects.filter(pk=input.session_id).exists():
            raise Exception('Invalid Session Id')

        slack_channel = SlackChannel.objects.create(**input)

        return CreateSlackChannelMutation(slack_channel=slack_channel)


class CreateSlackTeamSettingMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamSettingInputType(required=True)

    slack_team_setting = graphene.Field(SlackTeamSettingType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        slack_team_setting = SlackTeamSetting.objects.create(**input)

        return CreateSlackTeamSettingMutation(slack_team_setting=slack_team_setting)


class CreateSlackTeamInstallationMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInstallationInputType(required=True)

    slack_team_installation = graphene.Field(SlackTeamInstallationType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        slack_team_installation = SlackTeamInstallation.objects.create(**input)

        return CreateSlackTeamInstallationMutation(slack_team_installation=slack_team_installation)


class CreateMessageFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = MessageFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackUser.objects.filter(pk=input['slack_user_id']).exists():
            raise Exception('Invalid Slack User Id')

        if not SlackChannel.objects.filter(pk=input['slack_channel_id']).exists():
            raise Exception('Invalid Slack Channel Id')

        ts = input.pop('slack_event_ts')
        slack_event = SlackEvent.objects.create(ts=ts)

        session = Session.objects.get(slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slackuser__id=input['slack_user_id'])
        message = Message.objects.create(text=input['text'], session=session, author=author,
                                         time=input['time'], slack_event=slack_event)
        session.participants.add(author)

        return CreateMessageFromSlackMutation(slack_event=slack_event, message=message)


class CreateReplyFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = ReplyFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackUser.objects.filter(pk=input['slack_user_id']).exists():
            raise Exception('Invalid Slack User Id')

        if not SlackChannel.objects.filter(pk=input['slack_channel_id']).exists():
            raise Exception('Invalid Slack Channel Id')

        if not Message.objects.filter(slack_event__ts=input['message_slack_event_ts'],
                                      session__slackchannel__id=input['slack_channel_id']).exists():
            raise Exception('Invalid Message Slack Event Ts')

        ts = input.pop('slack_event_ts')
        slack_event = SlackEvent.objects.create(ts=ts)
        message = Message.objects.get(slack_event__ts=input['message_slack_event_ts'],
                                      session__slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slackuser__id=input['slack_user_id'])
        reply = Reply.objects.create(text=input['text'], message=message, author=author,
                                     time=input['time'], slack_event=slack_event)
        message.session.participants.add(author)

        return CreateReplyFromSlackMutation(slack_event=slack_event, reply=reply)


class CreateSessionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = SessionFromSlackInputType(required=True)

    session = graphene.Field(SessionType)
    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        session_args = input.pop('session', {})
        session = Session.objects.create(**session_args)
        channel = SlackChannel.objects.create(**input, session_id=session.id)

        return CreateSessionFromSlackMutation(session=session, slack_channel=channel)


class GetOrCreateUserFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input['slack_team_id']).exists():
            raise Exception('Invalid Slack Team Id')

        if SlackUser.objects.filter(id=input['id'], slack_team__id=input['slack_team_id']).exists():
            raise Exception(f'''Slack User with id {input['id']} already exists''')

        slack_team = SlackTeam.objects.get(pk=input['slack_team_id'])
        user, created = User.objects.get_or_create(email=input['email'],
                                                   defaults=dict(username=input['display_name'],
                                                                 first_name=input.get('first_name'),
                                                                 last_name=input.get('last_name'),
                                                                 avatar_url=input.get('avatar_72')))
        slack_team.group.members.add(user)
        slack_user = SlackUser.objects.create(**input, user=user)

        return GetOrCreateUserFromSlackMutation(user=user, slack_user=slack_user)


class GetOrCreateGroupFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = GroupFromSlackInputType(required=True)

    group = graphene.Field(GroupType)
    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if SlackTeam.objects.filter(pk=input['slack_team_id']).exists():
            raise Exception(f'''Slack Team with id {input['slack_team_id']} already exists''')

        group_name = input.pop('group_name')
        group, created = Group.objects.get_or_create(name=group_name)
        slack_team = SlackTeam.objects.create(id=input['slack_team_id'], name=input['slack_team_name'], group=group)

        return GetOrCreateGroupFromSlackMutation(group=group, slack_team=slack_team)


class SolveQuestionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = SolveQuestionFromSlackInputType(required=True)

    question = graphene.Field(QuestionType)
    session = graphene.Field(SessionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackChannel.objects.filter(id=input['slack_channel_id']).exists():
            raise Exception('Invalid Slack Channel Id')

        if not SlackUser.objects.filter(id=input['slack_user_id']).exists():
            raise Exception('Invalid Slack User Id')

        user = User.objects.get(slackuser__id=input['slack_user_id'])

        question = Question.objects.get(session__slackchannel__id=input['slack_channel_id'])
        question.is_solved = True
        question.solver = user
        question.save()

        session = question.session
        session.time_end = input['time_end']
        session.save()

        return SolveQuestionFromSlackMutation(question=question, session=session)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()
    create_slack_team_setting = CreateSlackTeamSettingMutation.Field()
    create_slack_team_installation = CreateSlackTeamInstallationMutation.Field()

    create_message_from_slack = CreateMessageFromSlackMutation.Field()
    create_reply_from_slack = CreateReplyFromSlackMutation.Field()

    create_session_from_slack = CreateSessionFromSlackMutation.Field()

    get_or_create_user_from_slack = GetOrCreateUserFromSlackMutation.Field()
    get_or_create_group_from_slack = GetOrCreateGroupFromSlackMutation.Field()

    solve_question_from_slack = SolveQuestionFromSlackMutation.Field()
