# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 23:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_auto_20160719_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='regular_player',
            field=models.BooleanField(default=True),
        ),
    ]