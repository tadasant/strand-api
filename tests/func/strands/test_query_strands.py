import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryStrands:

    @pytest.mark.django_db
    def test_get_strand(self, client, strand_factory):
        strand = strand_factory()

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['strand']['title']

    @pytest.mark.django_db
    def test_get_strands(self, client, strand_factory):
        strand_factory()
        strand_factory()

        query = QueryGenerator.get_strands()
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(response.json()['data']['strands']) == 2
