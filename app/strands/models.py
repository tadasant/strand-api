from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

from app.groups.models import Group
from app.users.models import User


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Strand(TimeStampedModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(default=now())

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='strands')
    owner = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='strands')
    tags = models.ManyToManyField(to=Tag, related_name='strands')

    def add_tags(self, tags):
        for tag_to_add in tags:
            tag, _ = Tag.objects.get_or_create(**tag_to_add)
            self.tags.add(tag)

    def __str__(self):
        return self.title
