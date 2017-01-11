# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 23:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0009_league_regular_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='regular_player',
        ),
        migrations.AddField(
            model_name='league',
            name='players',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='league',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]