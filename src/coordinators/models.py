from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from locations.models import District

class Coordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField()
    district = models.ForeignKey(District, verbose_name=_('District'),
            blank=True, null=True)

def filter_by_district(qs, user, lookup):
    # superusers and managers see everything
    if (user.is_superuser
            or hasattr(user, 'coordinator') and user.coordinator.is_manager):
        return qs
    # don't show anything to unconfigured users
    if not hasattr(user, 'coordinator') or not user.coordinator.district:
        return qs.none()
    kwargs = {
        lookup: user.coordinator.district
    }
    return qs.filter(**kwargs)
