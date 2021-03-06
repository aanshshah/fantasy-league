# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import league.models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0029_auto_20160803_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='duration_between_games',
            field=models.IntegerField(blank=True, default=7, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='games_in_season',
            field=models.IntegerField(blank=True, default=7, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='pairings',
            field=league.models.ListField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='start_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
