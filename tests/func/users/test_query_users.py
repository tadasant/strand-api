import pytest


class TestQueryUsers:

    @pytest.mark.django_db
    def test_get_user_unauthorized_fields(self, client, query_generator, user_factory):
        user = user_factory()

        query = query_generator.get_user_authorized(user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert not response.json()['data']['user']['slackUsers']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_user_public_fields(self, client, query_generator, user_factory):
        user = user_factory()

        query = query_generator.get_user(user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['user']['alias'] == user.alias

    @pytest.mark.django_db
    def test_get_users_authorized_fields(self, auth_client, query_generator, user_factory):
        user_factory()
        user_factory()

        query = query_generator.get_users_authorized()
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['users']) == 3
