from enum import Enum

from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from app.groups.models import Group
from app.users.models import User


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Topic(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    is_private = models.BooleanField(default=True)

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='topics')
    group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(to=Tag, related_name='topics')

    def add_or_create_tags(self, tags):
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            self.tags.add(tag)

    def __str__(self):
        return f'"{self.title}"'


class DiscussionStatus(Enum):
    OPEN = 'OPEN'
    STALE = 'STALE'
    PENDING_CLOSED = 'PENDING CLOSED'
    CLOSED = 'CLOSED'


class Discussion(TimeStampedModel):
    time_start = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(null=True)
    status = FSMField(default=DiscussionStatus.OPEN.value, protected=True)
    topic = models.OneToOneField(to=Topic, on_delete=models.CASCADE)
    participants = models.ManyToManyField(to=User, related_name='discussions')

    @property
    def datetime_of_last_non_bot_message(self):
        # TODO: Not factoring in replies
        last_non_bot_message = self.messages.filter(author__is_bot=False).order_by('time').last()
        if last_non_bot_message:
            return last_non_bot_message.time
        return self.time_start

    @property
    def minutes_since_last_non_bot_message(self):
        minutes = (
                round(((timezone.now() - self.datetime_of_last_non_bot_message).seconds / 60), 2) +
                ((timezone.now() - self.datetime_of_last_non_bot_message).days * 24 * 60)
        )
        return minutes

    @property
    def is_closed(self):
        return self.status == DiscussionStatus.CLOSED.value

    @property
    def is_pending_closed(self):
        return self.status == DiscussionStatus.PENDING_CLOSED.value

    @property
    def is_stale(self):
        return self.status == DiscussionStatus.STALE.value

    def standby_to_auto_close(self):
        self.mark_as_pending_closed()
        self.save()

    @transition(field=status, source=[DiscussionStatus.STALE.value, DiscussionStatus.PENDING_CLOSED.value],
                target=DiscussionStatus.OPEN.value, custom={'button_name': 'Mark as Open'})
    def mark_as_open(self):
        pass

    @transition(field=status, source='*', target=DiscussionStatus.STALE.value, custom={'button_name': 'Mark as Stale'})
    def mark_as_stale(self):
        pass

    @transition(field=status, source=DiscussionStatus.STALE.value, target=DiscussionStatus.PENDING_CLOSED.value,
                custom={'button_name': 'Mark as Pending Closed'})
    def mark_as_pending_closed(self):
        pass

    @transition(field=status, source='*', target=DiscussionStatus.CLOSED.value,
                custom={'button_name': 'Mark as Closed'})
    def mark_as_closed(self):
        self.time_end = timezone.now()

    def __str__(self):
        return f'Discussion for "{self.topic.title}"'
