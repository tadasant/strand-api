import pytest
import responses

from tests.resources.QueryGenerator import QueryGenerator


class TestSearch:
    # TODO: Aggressive testing of searching body, title, and tags in E2E test
    @pytest.mark.django_db
    def test_search(self, algolia, user_client, strand_factory):
        jimmy = user_client.user
        strand = strand_factory(saver=jimmy)
        assert len(algolia.calls) == 1, 'Index not executed'

        query = QueryGenerator.search(query=strand.title.split(' ')[0])
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(algolia.calls) == 2, 'Search not executed'
