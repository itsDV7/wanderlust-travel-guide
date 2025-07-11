# Generated by Django 4.2.23 on 2025-07-06 03:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_savedlocation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='savedlocation',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='savedlocation',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='place_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='types',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='savedlocation',
            name='user_ratings_total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='savedlocation',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='savedlocation',
            unique_together={('user', 'place_id')},
        ),
        migrations.RemoveField(
            model_name='savedlocation',
            name='place_type',
        ),
    ]
