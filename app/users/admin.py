from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from app.users.models import User


@admin.register(User)
class UserAdmin(GuardedModelAdmin):
    list_display = ('username', 'email')
