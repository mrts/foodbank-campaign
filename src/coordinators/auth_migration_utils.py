def get_coordinators_group(apps):
    return get_group(apps, 'Koordinaatorid')

def get_administrators_group(apps):
    return get_group(apps, 'Administraatorid')

def get_group(apps, name):
    Group = apps.get_model('auth', 'Group')
    return Group.objects.get(name=name)

def get_permissions(apps, *args):
    Permission = apps.get_model('auth', 'Permission')
    permissions = []
    for app_name, model_name, prefixes in args:
        permissions.extend(
            get_permission_objects(Permission, app_name, model_name, prefixes)
        )
    return permissions

def get_permission_objects(Permission, app_name, model_name, prefixes):
    permission_names = map(lambda prefix: prefix + '_' + model_name, prefixes)
    return list(Permission.objects.filter(
            codename__in=permission_names,
            content_type__app_label=app_name))
