import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryUsers:

    @pytest.mark.django_db
    def test_get_user_unauthorized_fields(self, client, user_factory):
        user = user_factory()

        query = QueryGenerator.get_user_authorized(user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['user']['slackUsers']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_user_public_fields(self, client, user_factory):
        user = user_factory()

        query = QueryGenerator.get_user(user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['user']['alias'] == user.alias

    @pytest.mark.django_db
    def test_get_users_authorized_fields(self, auth_client, user_factory):
        user_factory()
        user_factory()

        query = QueryGenerator.get_users_authorized()
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['users']) == 3
