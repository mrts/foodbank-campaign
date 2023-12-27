from django.db import models
from django.utils.translation import gettext_lazy as _


class District(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    send_thank_you_email = models.BooleanField(_("Send 'Thank You' email"),
        default=False)
    thank_you_email_template = models.TextField(_("'Thank You' email message"),
        blank=True)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('District'))
    address = models.CharField(_('Address'), max_length=255)
    contact_person = models.CharField(_('Contact person'), max_length=255,
            blank=True)

    class Meta:
        unique_together = ('district', 'name')
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']

    def __str__(self):
        return self.name
