# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-20 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20160820_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaignlocationshiftvolunteers',
            options={'verbose_name_plural': 'Campaing location shift volunteers'},
        ),
        migrations.AddField(
            model_name='campaignlocationshift',
            name='total_places',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
