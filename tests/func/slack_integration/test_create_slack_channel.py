import pytest


class TestCreateSlackChannel:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, mutation_generator, slack_channel_factory, slack_team_factory,
                             discussion_factory):
        discussion = discussion_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_slack_channel(id=slack_channel.id, name=slack_channel.name,
                                                           slack_team_id=slack_team.id, discussion_id=discussion.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, mutation_generator, slack_channel_factory, slack_team_factory,
                          discussion_factory):
        discussion = discussion_factory()
        slack_team = slack_team_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_slack_channel(id=slack_channel.id, name=slack_channel.name,
                                                           slack_team_id=slack_team.id, discussion_id=discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, mutation_generator, slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_slack_channel(id=slack_channel.id, name=slack_channel.name,
                                                           slack_team_id=slack_team.id, discussion_id=0)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == "{'discussion_id': ['Invalid pk \"0\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, mutation_generator, slack_channel_factory, slack_team_factory,
                   discussion_factory):
        discussion = discussion_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = mutation_generator.create_slack_channel(id=slack_channel.id, name=slack_channel.name,
                                                           slack_team_id=slack_team.id, discussion_id=discussion.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel']['slackChannel']['name'] == slack_channel.name
