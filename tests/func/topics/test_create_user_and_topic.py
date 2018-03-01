import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserAndTopic:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory.build()
        topic = topic_factory.build()

        mutation = MutationGenerator.create_user_and_topic(email=user.email, username=user.username,
                                                           first_name=user.first_name, last_name=user.last_name,
                                                           avatar_url=user.avatar_url, is_bot=str(user.is_bot).lower(),
                                                           groups=[group],
                                                           title=topic.title, description=topic.description,
                                                           is_private=str(topic.is_private).lower(),
                                                           group_id=group.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndTopic']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build()

        mutation = MutationGenerator.create_user_and_topic(email=user.email, username=user.username,
                                                           first_name=user.first_name, last_name=user.last_name,
                                                           avatar_url=user.avatar_url, is_bot=str(user.is_bot).lower(),
                                                           groups=[group],
                                                           title=topic.title, description=topic.description,
                                                           is_private=str(topic.is_private).lower(),
                                                           group_id=group.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndTopic']
        assert response.json()['errors'][0]['message'] == \
            str({'email': ['user with this email address already exists.']})

    @pytest.mark.django_db
    def test_invalid_group(self, auth_client, group_factory, topic_factory, user_factory):
        group = group_factory()
        user = user_factory.build()
        topic = topic_factory.build()

        mutation = MutationGenerator.create_user_and_topic(email=user.email, username=user.username,
                                                           first_name=user.first_name, last_name=user.last_name,
                                                           avatar_url=user.avatar_url, is_bot=str(user.is_bot).lower(),
                                                           groups=[group],
                                                           title=topic.title, description=topic.description,
                                                           is_private=str(topic.is_private).lower(),
                                                           group_id=group.id + 1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndTopic']
        assert response.json()['errors'][0]['message'] == \
            str({'group_id': [f'Invalid pk "{group.id + 1}" - object does not exist.']})

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_user_and_topic(email=user.email, username=user.username,
                                                           first_name=user.first_name, last_name=user.last_name,
                                                           avatar_url=user.avatar_url, is_bot=str(user.is_bot).lower(),
                                                           groups=[group],
                                                           title=topic.title, description=topic.description,
                                                           is_private=str(topic.is_private).lower(),
                                                           group_id=group.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndTopic']['topic']['title'] == topic.title
        assert response.json()['data']['createUserAndTopic']['user']['groups'][0]['name'] == group.name
