# Generated by Django 2.0.1 on 2018-01-11 01:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='time_start',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 1, 41, 44, 845576)),
        ),
    ]
