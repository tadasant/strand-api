# Generated by Django 2.0.2 on 2018-02-01 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slack_integration', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='slackteam',
            name='slack_agent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='slack_team', to='slack_integration.SlackAgent'),
        ),
        migrations.AddField(
            model_name='slackchannel',
            name='discussion',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='topics.Discussion'),
        ),
        migrations.AddField(
            model_name='slackchannel',
            name='slack_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_channels', to='slack_integration.SlackTeam'),
        ),
        migrations.AddField(
            model_name='slackapplicationinstallation',
            name='installer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='slack_integration.SlackUser'),
        ),
        migrations.AddField(
            model_name='slackapplicationinstallation',
            name='slack_agent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='slack_application_installation', to='slack_integration.SlackAgent'),
        ),
    ]