import pytest


class TestCreateUser:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, user_factory):
        user = user_factory.build()

        mutation = mutation_generator.create_user(email=user.email, username=user.username)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, user_factory):
        user = user_factory.build()

        mutation = mutation_generator.create_user(email=user.email, username=user.username)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser']['user']['alias']
