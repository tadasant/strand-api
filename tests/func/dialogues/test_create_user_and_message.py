import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserAndMessage:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory, message_factory, user_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_user_and_message(email=user.email,
                                                             username=user.username,
                                                             first_name=user.first_name,
                                                             last_name=user.last_name,
                                                             groups=[],
                                                             text=message.text,
                                                             discussion_id=discussion.id,
                                                             time=message.time)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndMessage']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, discussion_factory, message_factory, user_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_user_and_message(email=user.email,
                                                             username=user.username,
                                                             first_name=user.first_name,
                                                             last_name=user.last_name,
                                                             groups=[],
                                                             text=message.text,
                                                             discussion_id=discussion.id + 1,
                                                             time=message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndMessage']
        assert response.json()['errors'][0]['message'] == \
            str({'discussion_id': [f'Invalid pk "{discussion.id + 1}" - object does not exist.']})

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, discussion_factory, message_factory, user_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory()
        message = message_factory.build()

        mutation = MutationGenerator.create_user_and_message(email=user.email,
                                                             username=user.username,
                                                             first_name=user.first_name,
                                                             last_name=user.last_name,
                                                             groups=[],
                                                             text=message.text,
                                                             discussion_id=discussion.id,
                                                             time=message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndMessage']
        assert response.json()['errors'][0]['message'] == \
            str({'email': ['user with this email address already exists.']})

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory, message_factory, user_factory):
        discussion = discussion_factory(topic__is_private=False)
        user = user_factory.build()
        message = message_factory.build()

        mutation = MutationGenerator.create_user_and_message(email=user.email,
                                                             username=user.username,
                                                             first_name=user.first_name,
                                                             last_name=user.last_name,
                                                             groups=[],
                                                             text=message.text,
                                                             discussion_id=discussion.id,
                                                             time=message.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndMessage']['user']['id']
        assert response.json()['data']['createUserAndMessage']['message']['text'] == message.text
