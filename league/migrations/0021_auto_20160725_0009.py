# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-25 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0020_trade_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade_notification',
            name='notification_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='trade_notification',
            name='date_accepted',
            field=models.DateTimeField(default=None),
        ),
        migrations.RemoveField(
            model_name='trade_notification',
            name='player_traded',
        ),
        migrations.AddField(
            model_name='trade_notification',
            name='player_traded',
            field=models.ManyToManyField(to='league.Player'),
        ),
        migrations.AlterField(
            model_name='trade_notification',
            name='trade_status',
            field=models.BooleanField(default=False),
        ),
    ]
