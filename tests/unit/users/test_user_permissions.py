import pytest


class TestUserPermissions:
    @pytest.mark.django_db
    def test_user(self, user_factory):
        jimmy = user_factory()

        assert jimmy.has_perm('view_user', jimmy)
        assert jimmy.has_perm('change_user', jimmy)
        assert jimmy.has_perm('delete_user', jimmy)

    @pytest.mark.django_db
    def test_user_in_team(self, user_factory, team_factory):
        jimmy = user_factory()
        bobby = user_factory()
        team_factory(members=[jimmy, bobby])

        assert jimmy.has_perm('view_user', bobby)
        assert not jimmy.has_perm('change_user', bobby)
        assert not jimmy.has_perm('delete_user', bobby)

        assert bobby.has_perm('view_user', jimmy)
        assert not bobby.has_perm('change_user', jimmy)
        assert not bobby.has_perm('delete_user', jimmy)

    @pytest.mark.django_db
    def test_user_other_team(self, user_factory):
        jimmy = user_factory()
        bobby = user_factory()

        assert not jimmy.has_perm('view_user', bobby)
        assert not jimmy.has_perm('change_user', bobby)
        assert not jimmy.has_perm('delete_user', bobby)

        assert not bobby.has_perm('view_user', jimmy)
        assert not bobby.has_perm('change_user', jimmy)
        assert not bobby.has_perm('delete_user', jimmy)
