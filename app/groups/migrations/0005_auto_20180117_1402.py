# Generated by Django 2.0.1 on 2018-01-17 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_groupsetting_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupsetting',
            old_name='type',
            new_name='datatype',
        ),
    ]