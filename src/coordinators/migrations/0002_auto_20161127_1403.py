# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-27 12:03
from __future__ import unicode_literals

from django.db import migrations

# TODO: should add rights first with a migration :)
def remove_location_and_shift_add_delete_rights(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    coordinators_group = Group.objects.get(name='Koordinaatorid')
    permissions = (
            get_permissions(Permission, 'location', 'locations') +
            get_permissions(Permission, 'campaignlocationshift', 'campaigns')
    )
    coordinators_group.permissions.remove(*permissions)

def get_permissions(Permission, model_name, app_name):
    permission_names = ['add_' + model_name, 'delete_' + model_name]
    return list(Permission.objects.filter(
            codename__in=permission_names,
            content_type__app_label=app_name))


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('coordinators', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_location_and_shift_add_delete_rights),
    ]
