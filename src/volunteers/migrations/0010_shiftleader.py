# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0009_auto_20161102_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftLeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('phone', models.CharField(max_length=100, verbose_name='Phone')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Shift leader',
                'verbose_name_plural': 'Shift leaders',
            },
        ),
    ]
