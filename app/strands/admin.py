from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from app.strands.models import Strand, Tag


@admin.register(Strand)
class StrandAdmin(GuardedModelAdmin):
    list_display = ('title', 'original_poster', 'owner')


@admin.register(Tag)
class TagAdmin(GuardedModelAdmin):
    list_display = ('name',)
