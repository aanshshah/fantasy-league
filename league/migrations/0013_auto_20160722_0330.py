# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 03:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('league', '0012_league_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('rater', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='league',
            name='admin',
        ),
        migrations.AddField(
            model_name='league',
            name='special_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='league.SpecialUser'),
        ),
    ]
