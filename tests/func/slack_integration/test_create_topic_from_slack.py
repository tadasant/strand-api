import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateTopicFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_topic_from_slack(title=topic.title, description=topic.description,
                                                             is_private=str(topic.is_private).lower(),
                                                             original_poster_slack_user_id=slack_user.id,
                                                             tags=[tag_one, tag_two])
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_original_poster_slack_user(self, auth_client, topic_factory,
                                                slack_user_factory, tag_factory):
        slack_user = slack_user_factory.build()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_topic_from_slack(title=topic.title, description=topic.description,
                                                             is_private=str(topic.is_private).lower(),
                                                             original_poster_slack_user_id=slack_user.id,
                                                             tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'SlackUser matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build(is_private=False)

        mutation = MutationGenerator.create_topic_from_slack(title=topic.title, description=topic.description,
                                                             is_private=str(topic.is_private).lower(),
                                                             original_poster_slack_user_id=slack_user.id,
                                                             tags=[tag_one, tag_two])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['createTopicFromSlack']['topic']['tags']) == 2
        assert response.json()['data']['createTopicFromSlack']['topic']['title'] == topic.title
