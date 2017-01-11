# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-23 05:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0019_auto_20160722_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade_Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField()),
                ('date_accepted', models.DateTimeField()),
                ('trade_status', models.BooleanField()),
                ('player_traded', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Player')),
                ('user_requesting_trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]