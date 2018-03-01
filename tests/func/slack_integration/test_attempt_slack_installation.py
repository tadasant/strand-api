import pytest


class TestAttemptSlackInstallation:

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['invalid_token'], indirect=True)
    @pytest.mark.usefixtures('slack_oauth_request')
    def test_invalid_token(self, client, mutation_generator):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        client_id = '123456789012.123456789012.123456'
        redirect_uri = 'www.app.trystrand.com/install'

        mutation = mutation_generator.attempt_slack_installation(code, client_id, redirect_uri)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Error accessing OAuth: invalid_code'

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['valid_token'], indirect=True)
    @pytest.mark.usefixtures('slack_client', 'slack_oauth_request')
    def test_valid(self, client, mutation_generator):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        client_id = '123456789012.123456789012.123456'
        redirect_uri = 'www.app.trystrand.com/install'

        mutation = mutation_generator.attempt_slack_installation(code, client_id, redirect_uri)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['attemptSlackInstallation']['slackTeam']['name'] == 'Clippy Sandbox'
