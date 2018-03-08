import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryTags:

    @pytest.mark.django_db
    def test_get_tag(self, client, tag_factory):
        tag = tag_factory()

        query = QueryGenerator.get_tag(tag_name=tag.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['tag']['name']

    @pytest.mark.django_db
    def test_get_tags(self, client, tag_factory):
        tag_factory()
        tag_factory()

        query = QueryGenerator.get_tags()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['tags']) == 2
