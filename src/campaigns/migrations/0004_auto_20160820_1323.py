# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-20 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0001_initial'),
        ('campaigns', '0003_auto_20160820_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignlocationshiftvolunteers',
            name='campaign_location_shift',
        ),
        migrations.RemoveField(
            model_name='campaignlocationshiftvolunteers',
            name='volunteers',
        ),
        migrations.AddField(
            model_name='campaignlocationshift',
            name='volunteers',
            field=models.ManyToManyField(to='volunteers.Volunteer'),
        ),
        migrations.DeleteModel(
            name='CampaignLocationShiftVolunteers',
        ),
    ]
