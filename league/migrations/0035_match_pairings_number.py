# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-16 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0034_auto_20160816_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='match_pairings',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]