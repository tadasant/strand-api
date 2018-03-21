import pytest


class TestTeamPermissions:
    @pytest.mark.django_db
    def test_user_in_team(self, user_factory, team_factory):
        jimmy = user_factory()
        team = team_factory(members=[jimmy])

        assert jimmy.has_perm('view_team', team)
        assert not jimmy.has_perm('change_team', team)
        assert not jimmy.has_perm('delete_team', team)

    @pytest.mark.django_db
    def test_user_not_in_team(self, user_factory, team_factory):
        jimmy = user_factory()
        team = team_factory()

        assert not jimmy.has_perm('view_team', team)
        assert not jimmy.has_perm('change_team', team)
        assert not jimmy.has_perm('delete_team', team)
