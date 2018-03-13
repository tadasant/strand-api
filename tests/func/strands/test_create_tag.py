import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateTag:
    # TODO: Break out creating tags as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, tag_factory):
        mutation = MutationGenerator.create_tag(name=tag_factory.build().name)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createTag']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_name(self, superuser_client, tag_factory):
        mutation = MutationGenerator.create_tag(name=tag_factory().name)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createTag']
        assert response.json()['errors'][0]['message'] == str({'name': ['tag with this name already exists.']})

    @pytest.mark.django_db
    def test_valid(self, superuser_client, tag_factory):
        tag = tag_factory.build()
        mutation = MutationGenerator.create_tag(name=tag.name)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTag']['tag']['name'] == tag.name
