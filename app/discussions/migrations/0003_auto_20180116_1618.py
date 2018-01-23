# Generated by Django 2.0.1 on 2018-01-16 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0002_auto_20180115_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='slack_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message',
                                    to='slack_integration.SlackEvent'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='slack_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply',
                                    to='slack_integration.SlackEvent'),
        ),
    ]