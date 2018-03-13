import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateStrand:
    # TODO: Break out creating strands as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, strand_factory, user_factory, team_factory):
        saver = user_factory()
        owner = team_factory()
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=saver.id,
                                                   owner_id=owner.id)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_saver(self, superuser_client, user_factory, team_factory, strand_factory):
        jimmy = user_factory()
        owner = team_factory(members=[jimmy])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=jimmy.id + 1,
                                                   owner_id=owner.id)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == str({'saver_id':
                                                               [f'Invalid pk "{jimmy.id + 1}" '
                                                                f'- object does not exist.']
                                                               })

    @pytest.mark.django_db
    def test_invalid_owner(self, superuser_client, user_factory, team_factory, strand_factory):
        jimmy = user_factory()
        owner = team_factory(members=[jimmy])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=jimmy.id,
                                                   owner_id=owner.id + 1)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['createStrand']
        assert response.json()['errors'][0]['message'] == str({'owner_id':
                                                               [f'Invalid pk "{owner.id + 1}" '
                                                                f'- object does not exist.']
                                                               })

    @pytest.mark.django_db
    def test_valid_add_existing_tags(self, superuser_client, user_factory, team_factory, strand_factory, tag_factory):
        jimmy = user_factory()
        owner = team_factory(members=[jimmy])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=jimmy.id,
                                                   owner_id=owner.id,
                                                   tags=[tag_factory().name, tag_factory().name])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
        assert len(response.json()['data']['createStrand']['strand']['tags']) == 2

    @pytest.mark.django_db
    def test_valid_create_new_tags(self, superuser_client, user_factory, team_factory, strand_factory, tag_factory):
        jimmy = user_factory()
        owner = team_factory(members=[jimmy])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=jimmy.id,
                                                   owner_id=owner.id,
                                                   tags=[tag_factory.build().name, tag_factory.build().name])
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
        assert len(response.json()['data']['createStrand']['strand']['tags']) == 2

    @pytest.mark.django_db
    def test_valid(self, superuser_client, user_factory, team_factory, strand_factory):
        jimmy = user_factory()
        owner = team_factory(members=[jimmy])
        strand = strand_factory.build()

        mutation = MutationGenerator.create_strand(title=strand.title,
                                                   body=strand.body,
                                                   timestamp=strand.timestamp,
                                                   saver_id=jimmy.id,
                                                   owner_id=owner.id)
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createStrand']['strand']['title']
