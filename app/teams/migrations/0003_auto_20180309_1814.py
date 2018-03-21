# Generated by Django 2.0.2 on 2018-03-09 18:14

import app.teams.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('teams', '0002_team_members'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'permissions': (('view_team', 'View team'),)},
        ),
        migrations.AddField(
            model_name='team',
            name='group',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=80, unique=True, validators=[app.teams.models.validate_team_name]),
        ),
    ]
