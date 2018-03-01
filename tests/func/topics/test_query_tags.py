import pytest


class TestQueryTags:

    @pytest.mark.django_db
    def test_get_tag(self, client, query_generator, tag_factory):
        tag = tag_factory()

        query = query_generator.get_tag(tag.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['tag']['id'] == str(tag.id)

    @pytest.mark.django_db
    def test_get_tags(self, client, query_generator, tag_factory):
        tag_factory()
        tag_factory()

        query = query_generator.get_tags()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['tags']) == 2
