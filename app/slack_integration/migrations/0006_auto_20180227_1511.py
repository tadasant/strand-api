# Generated by Django 2.0.2 on 2018-02-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogues', '0003_remove_reply_origin_slack_event'),
        ('slack_integration', '0005_auto_20180222_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='SlackEvent',
            name='message',
            field=models.OneToOneField(blank=True, null=True,
                                       on_delete=models.deletion.CASCADE,
                                       related_name='slack_event',
                                       to='dialogues.Message'),
            preserve_default=False
        ),
    ]
