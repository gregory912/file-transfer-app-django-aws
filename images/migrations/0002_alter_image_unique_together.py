# Generated by Django 4.1.7 on 2023-03-03 20:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('user', 'name')},
        ),
    ]
