# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-16 20:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0038_auto_20160816_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='match_pairings',
            name='users',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_match_details',
            name='user',
            field=models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]