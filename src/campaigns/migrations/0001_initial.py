# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('name', models.CharField(max_length=255)),
                ('locations', models.ManyToManyField(to='locations.Location')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignLocationShift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('volunteers', models.ManyToManyField(to='volunteers.Volunteer')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='campaign',
            unique_together=set([('start', 'name')]),
        ),
    ]
