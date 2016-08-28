from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from tinymce.models import HTMLField

from locations.models import Location
from volunteers.models import Volunteer


class Campaign(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    start = models.DateField(_('Start'))
    end = models.DateField(_('End'))
    is_active = models.BooleanField(_('Is active'))
    registration_form_header = HTMLField(_('Registration form header'))
    registration_form_footer = HTMLField(_('Registration form footer'))
    registration_form_right_panel = HTMLField(_('Registration form right panel'))

    class Meta:
        unique_together = ('start', 'name')
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')

    def __unicode__(self):
        return u'{start} {name}'.format(**self.__dict__)

    def clean(self):
        if (self.is_active and Campaign.objects
                .filter(is_active=True)
                .exclude(pk=self.pk) # works when pk is None, too
                .exists()):
            raise ValidationError('Only one campaign can be active at a time')


class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign, verbose_name=_('Campaign'))
    location = models.ForeignKey(Location, verbose_name=_('Location'))
    day = models.DateField(_('Day'))
    start = models.TimeField(_('Start'))
    end = models.TimeField(_('End'))
    total_places = models.IntegerField(_('Total places'))
    volunteers = models.ManyToManyField(Volunteer, blank=True,
            verbose_name=_('Volunteers'))

    class Meta:
        unique_together = ('campaign', 'location', 'day', 'start')
        verbose_name = _('Campaign shift')
        verbose_name_plural = _('Campaign shifts')

    def __unicode__(self):
        campaign = unicode(self.campaign)
        location = unicode(self.location)
        day = unicode(self.day)
        start = unicode(self.start)
        end = unicode(self.end)
        return u'{campaign} {location} {day} {start}-{end} vahetus'.format(**locals())
