import pytest

from tests.resources.QueryGenerator import QueryGenerator


class TestQueryStrands:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, strand_factory):
        jimmy = user_factory()
        strand = strand_factory(original_poster=jimmy)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['strand']

    @pytest.mark.django_db
    def test_get_user_strand(self, user_client, strand_factory):
        jimmy = user_client.user
        strand = strand_factory(original_poster=jimmy)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['strand']['title']

    @pytest.mark.django_db
    def test_get_team_strand(self, user_client, user_factory, team_factory, strand_factory):
        jimmy = user_client.user
        bobby = user_factory()
        team = team_factory(members=[jimmy, bobby])
        strand = strand_factory(original_poster=bobby, owner=team)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert response.json()['data']['strand']['title']

    @pytest.mark.django_db
    def test_get_other_strand(self, user_client, user_factory, strand_factory):
        bobby = user_factory()
        strand = strand_factory(original_poster=bobby)

        query = QueryGenerator.get_strand(strand_id=strand.id)
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['strand']

    @pytest.mark.django_db
    def test_get_strands(self, user_client, strand_factory, user_factory, team_factory):
        jimmy = user_client.user
        bobby = user_factory()
        team = team_factory(members=[jimmy, bobby])
        strand_factory(original_poster=bobby, owner=team)  # Same team
        strand_factory(original_poster=bobby)  # Different user, different team
        strand_factory(original_poster=jimmy)  # Same user

        query = QueryGenerator.get_strands()
        response = user_client.post('/graphql', {'query': query})

        assert response.status_code == 200, response.content
        assert len([strand for strand in response.json()['data']['strands'] if strand]) == 2
