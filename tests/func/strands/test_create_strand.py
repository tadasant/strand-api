import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateStrand:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, strand_factory, user_factory, group_factory):
        original_poster = user_factory()
        owner = group_factory(members=[original_poster])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id,
                                                   owner_id=owner.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_original_poster(self, auth_client, strand_factory, user_factory, group_factory):
        original_poster = user_factory()
        owner = group_factory()
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id + 1,
                                                   owner_id=owner.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == str({'original_poster_id':
                                                               [f'Invalid pk "{original_poster.id + 1}" '
                                                                f'- object does not exist.']
                                                               })

    @pytest.mark.django_db
    def test_invalid_owner(self, auth_client, strand_factory, user_factory, group_factory):
        original_poster = user_factory()
        owner = group_factory()
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id,
                                                   owner_id=owner.id + 1)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == str({'owner_id':
                                                               [f'Invalid pk "{owner.id + 1}" '
                                                                f'- object does not exist.']
                                                               })

    @pytest.mark.django_db
    def test_valid_add_existing_tags(self, auth_client, strand_factory, user_factory, group_factory, tag_factory):
        original_poster = user_factory()
        owner = group_factory(members=[original_poster])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id,
                                                   owner_id=owner.id,
                                                   tags=[tag_factory().name, tag_factory().name])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
        assert len(response.json()['data']['createStrand']['strand']['tags']) == 2

    @pytest.mark.django_db
    def test_valid_create_new_tags(self, auth_client, strand_factory, user_factory, group_factory, tag_factory):
        original_poster = user_factory()
        owner = group_factory(members=[original_poster])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id,
                                                   owner_id=owner.id,
                                                   tags=[tag_factory.build().name, tag_factory.build().name])
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
        assert len(response.json()['data']['createStrand']['strand']['tags']) == 2

    @pytest.mark.django_db
    def test_valid(self, auth_client, strand_factory, user_factory, group_factory):
        original_poster = user_factory()
        owner = group_factory(members=[original_poster])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   original_poster_id=original_poster.id,
                                                   owner_id=owner.id)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
