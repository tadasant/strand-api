import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateUserAndTopicFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, slack_user_factory, slack_team_factory,
                             tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_user_and_topic_from_slack(title=topic.title,
                                                                      description=topic.description,
                                                                      is_private=str(topic.is_private).lower(),
                                                                      id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_team.id,
                                                                      tags=[tag_one, tag_two])
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, topic_factory, slack_user_factory,
                                slack_team_factory, tag_factory):
        slack_user = slack_user_factory()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_user_and_topic_from_slack(title=topic.title,
                                                                      description=topic.description,
                                                                      is_private=str(topic.is_private).lower(),
                                                                      id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_team.id,
                                                                      tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, topic_factory, slack_user_factory,
                                slack_team_factory, tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory.build()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_user_and_topic_from_slack(title=topic.title,
                                                                      description=topic.description,
                                                                      is_private=str(topic.is_private).lower(),
                                                                      id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_team.id,
                                                                      tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, slack_user_factory, slack_team_factory,
                   tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_user_and_topic_from_slack(title=topic.title,
                                                                      description=topic.description,
                                                                      is_private=str(topic.is_private).lower(),
                                                                      id=slack_user.id,
                                                                      name=slack_user.name,
                                                                      first_name=slack_user.first_name,
                                                                      last_name=slack_user.last_name,
                                                                      real_name=slack_user.real_name,
                                                                      display_name=slack_user.display_name,
                                                                      email=slack_user.email,
                                                                      image_72=slack_user.image_72,
                                                                      is_bot=str(slack_user.is_bot).lower(),
                                                                      is_admin=str(slack_user.is_admin).lower(),
                                                                      slack_team_id=slack_team.id,
                                                                      tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createUserAndTopicFromSlack']['slackUser']['id'] == slack_user.id
        assert response.json()['data']['createUserAndTopicFromSlack']['topic']['title'] == topic.title
        assert len(response.json()['data']['createUserAndTopicFromSlack']['topic']['tags']) == 2
