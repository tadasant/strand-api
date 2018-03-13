import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryTags:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, tag_factory):
        tag = tag_factory()

        query = QueryGenerator.get_tag(tag_name=tag.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['tag']

    @pytest.mark.django_db
    def test_get_tag(self, user_client, tag_factory):
        tag = tag_factory()

        query = QueryGenerator.get_tag(tag_name=tag.name)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['tag']['name'] == tag.name

    @pytest.mark.django_db
    def test_get_tags(self, user_client, tag_factory):
        tag_factory()
        tag_factory()

        query = QueryGenerator.get_tags()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len([tag for tag in response.json()['data']['tags'] if tag]) == 2
