# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-28 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0025_auto_20160727_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='duration_between_games',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='league',
            name='games_in_season',
            field=models.IntegerField(default=7),
        ),
    ]
