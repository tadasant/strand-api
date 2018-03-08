import factory.fuzzy
from django.contrib.auth.hashers import make_password

from app.teams.models import Team
from app.users.models import User
from app.strands.models import Strand, Tag


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
    password = make_password('mypass123!')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

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


class StrandFactory(factory.DjangoModelFactory):
    class Meta:
        model = Strand

    title = factory.Faker('sentence')
    body = factory.Faker('sentence')
    original_poster = factory.SubFactory(UserFactory)
    owner = factory.SubFactory(TeamFactory)
