import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestChangePassword:
    # TODO: Break out creating tags as superuser vs regular user after v0.3

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory):
        user = user_factory()

        mutation = MutationGenerator.change_password(user_id=user.id, old_password='mypass123!',
                                                     new_password='ABC!')
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['changePassword']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_id(self, superuser_client, user_factory):
        user = user_factory()

        mutation = MutationGenerator.change_password(user_id=user.id + 1, old_password='mypass123!',
                                                     new_password='ABC!')
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['changePassword']
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_password(self, superuser_client, user_factory):
        user = user_factory()

        mutation = MutationGenerator.change_password(user_id=user.id, old_password='mypass123',
                                                     new_password='ABC!')
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert not response.json()['data']['changePassword']
        assert response.json()['errors'][0]['message'] == str({'old_password': ['Wrong password.']})

    @pytest.mark.django_db
    def test_valid(self, superuser_client, user_factory):
        user = user_factory()

        mutation = MutationGenerator.change_password(user_id=user.id, old_password='mypass123!',
                                                     new_password='ABC!')
        response = superuser_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['changePassword']['user']['email'] == user.email
