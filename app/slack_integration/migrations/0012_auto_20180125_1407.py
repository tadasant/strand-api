# Generated by Django 2.0.1 on 2018-01-25 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack_integration', '0011_auto_20180125_1350'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SlackTeamInstallation',
            new_name='SlackApplicationInstallation',
        ),
    ]