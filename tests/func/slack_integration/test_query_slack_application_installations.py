import pytest


class TestQuerySlackApplicationInstallations:

    @pytest.mark.django_db
    def test_get_slack_application_installation(self, auth_client, query_generator,
                                                slack_application_installation_factory):
        slack_application_installation = slack_application_installation_factory()

        query = query_generator.get_slack_application_installation(slack_application_installation.id)
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['slackApplicationInstallation']['botAccessToken'] == \
            slack_application_installation.bot_access_token

    @pytest.mark.django_db
    def test_get_slack_application_installations(self, auth_client, query_generator,
                                                 slack_application_installation_factory):
        slack_application_installation_factory()
        slack_application_installation_factory()

        query = query_generator.get_slack_application_installations()
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['slackApplicationInstallations']) == 2

    @pytest.mark.django_db
    def test_get_active_slack_application_installations(self, auth_client, query_generator, slack_agent_factory,
                                                        slack_application_installation_factory):
        slack_agent_one = slack_agent_factory(status='INITIATED')
        slack_application_installation_factory(slack_agent=slack_agent_one)
        slack_agent_two = slack_agent_factory(status='ACTIVE')
        slack_application_installation_factory(slack_agent=slack_agent_two)

        query = query_generator.get_active_slack_application_installations()
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['slackApplicationInstallations']) == 1
