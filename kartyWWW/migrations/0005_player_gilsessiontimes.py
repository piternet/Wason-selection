# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kartyWWW', '0004_auto_20180117_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='gilSessionTimes',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
