# Generated by Django 3.2.4 on 2021-06-30 16:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow_like_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='follower',
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ManyToManyField(related_name='fan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(related_name='influencer', to=settings.AUTH_USER_MODEL),
        ),
    ]