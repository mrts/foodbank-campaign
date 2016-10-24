from django.db import models
from django.utils.translation import ugettext_lazy as _


class District(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    district = models.ForeignKey(District, verbose_name=_('District'))
    address = models.CharField(_('Address'), max_length=255)

    class Meta:
        unique_together = ('district', 'name')
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']

    def __unicode__(self):
        return self.name
