import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserAndReply:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, reply_factory, user_factory):
        message = message_factory(discussion__topic__is_private=False)
        user = user_factory.build()
        reply = reply_factory.build()

        mutation = MutationGenerator.create_user_and_reply(email=user.email,
                                                           username=user.username,
                                                           first_name=user.first_name,
                                                           last_name=user.last_name,
                                                           groups=[],
                                                           text=reply.text,
                                                           message_id=message.id,
                                                           time=reply.time)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndReply']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_message(self, auth_client, message_factory, reply_factory, user_factory):
        message = message_factory(discussion__topic__is_private=False)
        user = user_factory.build()
        reply = reply_factory.build()

        mutation = MutationGenerator.create_user_and_reply(email=user.email,
                                                           username=user.username,
                                                           first_name=user.first_name,
                                                           last_name=user.last_name,
                                                           groups=[],
                                                           text=reply.text,
                                                           message_id=message.id + 1,
                                                           time=reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndReply']
        assert response.json()['errors'][0]['message'] == \
            str({'message_id': [f'Invalid pk "{message.id + 1}" - object does not exist.']})

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, message_factory, reply_factory, user_factory):
        message = message_factory(discussion__topic__is_private=False)
        user = user_factory()
        reply = reply_factory.build()

        mutation = MutationGenerator.create_user_and_reply(email=user.email,
                                                           username=user.username,
                                                           first_name=user.first_name,
                                                           last_name=user.last_name,
                                                           groups=[],
                                                           text=reply.text,
                                                           message_id=message.id,
                                                           time=reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createUserAndReply']
        assert response.json()['errors'][0]['message'] == \
            str({'email': ['user with this email address already exists.']})

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, reply_factory, user_factory):
        message = message_factory(discussion__topic__is_private=False)
        user = user_factory.build()
        reply = reply_factory.build()

        mutation = MutationGenerator.create_user_and_reply(email=user.email,
                                                           username=user.username,
                                                           first_name=user.first_name,
                                                           last_name=user.last_name,
                                                           groups=[],
                                                           text=reply.text,
                                                           message_id=message.id,
                                                           time=reply.time)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndReply']['user']['id']
        assert response.json()['data']['createUserAndReply']['reply']['message']['text'] == message.text
