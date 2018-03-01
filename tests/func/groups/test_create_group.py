import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateGroup:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, group_factory):
        group = group_factory.build()

        mutation = MutationGenerator.create_group(group.name)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createGroup'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, group_factory):
        group = group_factory.build()

        mutation = MutationGenerator.create_group(group.name)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createGroup']['group']['name'] == group.name
