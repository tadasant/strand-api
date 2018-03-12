import pytest


class TestStrandPermissions:
    @pytest.mark.django_db
    def test_user_strands(self, user_factory, strand_factory):
        jimmy = user_factory()
        strand = strand_factory(original_poster=jimmy)

        assert jimmy.has_perm('view_strand', strand)
        assert jimmy.has_perm('change_strand', strand)
        assert jimmy.has_perm('delete_strand', strand)

    @pytest.mark.django_db
    def test_user_team_strands(self, user_factory, team_factory, strand_factory):
        jimmy = user_factory()
        bobby = user_factory()
        same_team = team_factory(members=[jimmy, bobby])
        strand = strand_factory(original_poster=bobby, owner=same_team)

        assert jimmy.has_perm('view_strand', strand)
        assert not jimmy.has_perm('change_strand', strand)
        assert not jimmy.has_perm('delete_strand', strand)

    @pytest.mark.django_db
    def test_user_other_team_strands(self, user_factory, team_factory, strand_factory):
        jimmy = user_factory()
        bobby = user_factory()
        other_team = team_factory(members=[bobby])
        strand = strand_factory(original_poster=bobby, owner=other_team)

        assert not jimmy.has_perm('view_strand', strand)
        assert not jimmy.has_perm('change_strand', strand)
        assert not jimmy.has_perm('delete_strand', strand)
