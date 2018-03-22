import pytest

from tests.resources.MutationGenerator import MutationGenerator
from tests.resources.QueryGenerator import QueryGenerator


class TestUpdateStrand:
    # TODO: Break out creating strands as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, strand_factory, tag_factory):
        strand = strand_factory()
        new_title = strand_factory.build().title
        new_tag = tag_factory()

        mutation = MutationGenerator.update_strand(strand_id=strand.id,
                                                   title=new_title,
                                                   tags=[new_tag.name])
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['updateStrand']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_update_title(self, superuser_client, strand_factory):
        strand = strand_factory()
        new_title = strand_factory.build().title

        mutation = MutationGenerator.update_strand(strand_id=strand.id,
                                                   title=new_title)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['updateStrand']['strand']['title'] == new_title
        assert response.json()['data']['updateStrand']['strand']['body'] == strand.body

    @pytest.mark.django_db
    def test_update_tags(self, superuser_client, strand_factory, tag_factory):
        old_tag = tag_factory()
        strand = strand_factory(tags=[old_tag])
        new_tag = tag_factory.build()

        # Assert that old_tag exists
        query = QueryGenerator.get_tags()
        response = superuser_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['tags']) == 1
        assert response.json()['data']['tags'][0]['name'] == old_tag.name

        mutation = MutationGenerator.update_strand(strand_id=strand.id,
                                                   tags=[new_tag.name])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['updateStrand']['strand']['title'] == strand.title
        assert response.json()['data']['updateStrand']['strand']['body'] == strand.body
        assert response.json()['data']['updateStrand']['strand']['tags'][0]['name'] == new_tag.name

        # Assert that old_tag was orphaned and deleted
        query = QueryGenerator.get_tags()
        response = superuser_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['tags']) == 1
        assert response.json()['data']['tags'][0]['name'] == new_tag.name

