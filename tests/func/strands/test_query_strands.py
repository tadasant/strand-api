import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryStrands:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, strand_factory):
        jimmy = user_factory()
        strand = strand_factory(saver=jimmy)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['strand']

    @pytest.mark.django_db
    def test_get_user_strand(self, user_client, strand_factory):
        jimmy = user_client.user
        strand = strand_factory(saver=jimmy)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['strand']['title']

    @pytest.mark.django_db
    def test_get_team_strand(self, user_client, user_factory, team_factory, strand_factory):
        jimmy = user_client.user
        bobby = user_factory()
        team = team_factory(members=[jimmy, bobby])
        strand = strand_factory(saver=bobby, owner=team)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['strand']['title']

    @pytest.mark.django_db
    def test_get_other_strand(self, user_client, user_factory, strand_factory):
        bobby = user_factory()
        strand = strand_factory(saver=bobby)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['strand']

    @pytest.mark.django_db
    def test_get_strands(self, algolia, user_client, strand_factory, user_factory, team_factory):
        jimmy = user_client.user
        bobby = user_factory()
        team = team_factory(members=[jimmy, bobby])
        strand_factory(saver=bobby, owner=team)  # Same team
        strand_factory(saver=bobby)  # Different user, different team
        strand_factory(saver=jimmy)  # Same user
        assert len(algolia.calls) == 3, 'Strand was not indexed'

        query = QueryGenerator.get_strands()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len([strand for strand in response.json()['data']['strands'] if strand]) == 2
        assert len(algolia.calls) == 3, 'Search was mistakenly executed'

    @pytest.mark.django_db
    def test_get_strands_with_query(self, algolia, user_client, strand_factory):
        jimmy = user_client.user
        strand = strand_factory(saver=jimmy)
        assert len(algolia.calls) == 1, 'Strand was not indexed'

        query = QueryGenerator.get_strands(query=strand.title.split(' ')[0])
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len(algolia.calls) == 2, 'Search was not executed'
