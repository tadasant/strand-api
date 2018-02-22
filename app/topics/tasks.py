from django.conf import settings

from app.api.celery import celery_app
from app.topics.models import Discussion, DiscussionStatus
from app.slack_integration.wrappers import SlackAppClientWrapper


@celery_app.task
def mark_stale_discussions():
    """
    Task that changes discussions from OPEN to
    STALE after 30 minutes of inactivity.
    """
    discussions = Discussion.objects.filter(status=DiscussionStatus.OPEN.value).all()
    for discussion in discussions:
        if discussion.minutes_since_last_non_bot_message >= settings.MIN_UNTIL_STALE:
            discussion.mark_as_stale()
            discussion.save()
            if discussion.slack_channel:
                SlackAppClientWrapper.post_stale_discussion(discussion)


@celery_app.task
def auto_close_pending_closed_discussion(discussion_id):
    """
    Task that closes discussion that's been set to PENDING CLOSED
    if there is no new activity for 5 additional minutes.
    """
    discussion = Discussion.objects.get(pk=discussion_id)
    if discussion.is_pending_closed:
        discussion.mark_as_closed()
        discussion.save()
        if discussion.slack_channel:
            SlackAppClientWrapper.post_auto_closed_discussion(discussion)
