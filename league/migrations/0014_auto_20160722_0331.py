# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0013_auto_20160722_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='special_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.SpecialUser'),
        ),
    ]
