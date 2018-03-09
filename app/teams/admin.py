from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from app.teams.models import Team


@admin.register(Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ('name',)
