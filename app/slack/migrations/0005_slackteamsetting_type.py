# Generated by Django 2.0.1 on 2018-01-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0004_auto_20180117_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackteamsetting',
            name='type',
            field=models.CharField(choices=[('String', 'String'), ('Boolean', 'Boolean'), ('Number', 'Number')], default='String', max_length=7),
        ),
    ]
