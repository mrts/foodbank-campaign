# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-20 11:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_auto_20160820_1410'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='campaignlocationshift',
            unique_together=set([('campaign', 'location', 'day', 'start')]),
        ),
    ]
