# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 03:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0016_auto_20160722_0333'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TypeUser',
            new_name='SpecialUser',
        ),
    ]