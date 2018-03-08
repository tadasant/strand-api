from django.db import models
from model_utils.models import TimeStampedModel

from app.users.models import User


class Team(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(to=User, related_name='teams')

    class Meta:
        permissions = (
            ('view_team', 'View team'),  # add_team, change_team and delete_team are added by default
        )

    def __str__(self):
        return self.name
