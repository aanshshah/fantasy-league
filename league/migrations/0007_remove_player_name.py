# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-17 20:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0006_auto_20160717_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
    ]
