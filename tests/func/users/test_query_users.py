import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryUsers:
    @pytest.mark.django_db
    def test_get_me_unauthenticated(self, client, user_factory):
        query = QueryGenerator.get_me()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['me']

    @pytest.mark.django_db
    def test_get_me(self, user_client):
        query = QueryGenerator.get_me()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['me']['email'] == user_client.user.email

    @pytest.mark.django_db
    def test_get_user_unauthenticated(self, client, user_factory):
        user = user_factory()

        query = QueryGenerator.get_user(user_id=user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['user']

    @pytest.mark.django_db
    def test_get_user_by_id(self, user_client):
        jimmy = user_client.user

        query = QueryGenerator.get_user(user_id=jimmy.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['user']['id'] == str(jimmy.id)

    @pytest.mark.django_db
    def test_get_user_by_email(self, superuser_client, user_factory):
        jimmy = user_factory()

        query = QueryGenerator.get_user(email=jimmy.email)
        response = superuser_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['user']['email'] == jimmy.email

    @pytest.mark.django_db
    def test_get_users(self, user_client, user_factory, team_factory):
        jimmy = user_client.user
        bobby = user_factory()  # User in team
        user_factory()  # User not in team
        team_factory(members=[jimmy, bobby])

        query = QueryGenerator.get_users()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len([user for user in response.json()['data']['users'] if user]) == 2
