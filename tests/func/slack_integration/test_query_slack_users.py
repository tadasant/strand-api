import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQuerySlackUsers:

    @pytest.mark.django_db
    def test_get_slack_user_unauthorized(self, client, slack_user_factory):
        slack_user = slack_user_factory()

        query = QueryGenerator.get_slack_user(slack_user.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_slack_user(self, auth_client, slack_user_factory):
        slack_user = slack_user_factory()

        query = QueryGenerator.get_slack_user(slack_user.id)
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['slackUser']['displayName'] == slack_user.display_name

    @pytest.mark.django_db
    def test_get_slack_users_unauthorized(self, client, slack_user_factory):
        slack_user_factory()
        slack_user_factory()

        query = QueryGenerator.get_slack_users()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_slack_users(self, auth_client, slack_user_factory):
        slack_user_factory()
        slack_user_factory()

        query = QueryGenerator.get_slack_users()
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['slackUsers']) == 2
