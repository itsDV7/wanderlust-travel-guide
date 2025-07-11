# Generated by Django 4.2.23 on 2025-07-05 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandmarkImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Uploaded landmark image', upload_to='landmark_images/')),
                ('landmark_name', models.CharField(blank=True, max_length=255, null=True)),
                ('identified_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landmark_images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
