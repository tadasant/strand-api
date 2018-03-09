import pytest


class TestTagPermissions:
    @pytest.mark.django_db
    def test_tags(self, user_factory, tag_factory):
        jimmy = user_factory()
        tag = tag_factory()

        assert jimmy.has_perm('view_tag', tag)
        assert not jimmy.has_perm('change_tag', tag)
        assert not jimmy.has_perm('delete_tag', tag)
