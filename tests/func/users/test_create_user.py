import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUser:
    # TODO: Break out creating users as superuser vs anonymous user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory):
        user = user_factory.build()

        mutation = MutationGenerator.create_user(email=user.email, username=user.username)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUser'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, superuser_client, user_factory):
        user = user_factory.build()

        mutation = MutationGenerator.create_user(email=user.email, username=user.username)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUser']['user']['id']
