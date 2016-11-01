# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0010_shiftleader'),
        ('campaigns', '0010_auto_20161029_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignlocationshift',
            name='shift_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='volunteers.ShiftLeader', verbose_name='Shift leader'),
        ),
    ]
