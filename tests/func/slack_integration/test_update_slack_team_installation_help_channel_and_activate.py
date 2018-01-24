import pytest


class TestUpdateSlackTeamInstallationHelpChannelAndActivate:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_installation_factory):
        slack_team_installation = slack_team_installation_factory(help_channel_id=None)
        help_channel_id = slack_team_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackTeamInstallationHelpChannelAndActivate(
            input: {{slackTeamId: "{slack_team_installation.slack_team_id}", helpChannelId: "{help_channel_id}"}}) {{
              slackTeamInstallation {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackTeamInstallationHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, slack_team_factory, slack_team_installation_factory):
        slack_team = slack_team_factory.build()
        slack_team_installation_factory(help_channel_id=None)
        help_channel_id = slack_team_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackTeamInstallationHelpChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            helpChannelId: "{help_channel_id}"}}) {{
              slackTeamInstallation {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackTeamInstallationHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_team_installation_factory):
        slack_team_installation = slack_team_installation_factory(help_channel_id=None, is_active=False)
        help_channel_id = slack_team_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackTeamInstallationHelpChannelAndActivate(
            input: {{slackTeamId: "{slack_team_installation.slack_team_id}", helpChannelId: "{help_channel_id}"}}) {{
              slackTeamInstallation {{
                helpChannelId
                isActive
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackTeamInstallationHelpChannelAndActivate']['slackTeamInstallation'][
                   'helpChannelId'] == help_channel_id
        assert response.json()['data']['updateSlackTeamInstallationHelpChannelAndActivate']['slackTeamInstallation'][
            'isActive']