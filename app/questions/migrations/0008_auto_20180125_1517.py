# Generated by Django 2.0.1 on 2018-01-25 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20180125_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.Group'),
        ),
        migrations.AlterField(
            model_name='question',
            name='original_poster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asked_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='solver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solved_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]