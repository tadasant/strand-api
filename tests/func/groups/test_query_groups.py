import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryGroups:

    @pytest.mark.django_db
    def test_get_group(self, group_factory, client):
        group = group_factory()

        query = QueryGenerator.get_group(group.name)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['group']['id'] == str(group.id)

    @pytest.mark.django_db
    def test_get_groups(self, group_factory, client):
        group_factory()
        group_factory()

        query = QueryGenerator.get_groups()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['groups']) == 2
