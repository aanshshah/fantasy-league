# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-12 18:50
from __future__ import unicode_literals

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0032_auto_20160812_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='picture',
            field=s3direct.fields.S3DirectField(),
        ),
    ]