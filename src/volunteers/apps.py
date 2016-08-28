from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VolunteersConfig(AppConfig):
    name = 'volunteers'
    verbose_name = _('Volunteers')
