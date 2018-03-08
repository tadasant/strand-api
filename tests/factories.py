import factory.fuzzy
import pytz
from django.contrib.auth.hashers import make_password

from app.dialogues.models import Message, Reply
from app.groups.models import Group
from app.topics.models import Topic, Discussion, Tag, DiscussionStatus
from app.users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
    password = make_password('mypass123!')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker('company')

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')


class TopicFactory(factory.DjangoModelFactory):
    class Meta:
        model = Topic

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    is_private = factory.Faker('pybool')

    original_poster = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class DiscussionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Discussion

    status = DiscussionStatus.OPEN.value
    time_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    time_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)
    topic = factory.SubFactory(TopicFactory)

    @factory.post_generation
    def participants(self, create, extracted):
        if not create:
            return

        if extracted:
            for participant in extracted:
                self.participants.add(participant)


class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Message

    text = factory.Faker('sentence')
    discussion = factory.SubFactory(DiscussionFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)


class ReplyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reply

    text = factory.Faker('sentence')
    message = factory.SubFactory(MessageFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)
