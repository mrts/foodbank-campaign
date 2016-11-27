# coding: utf-8

import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.formats import date_format
from django.utils.dateformat import DateFormat
from django.utils.html import format_html
from django.conf import settings

from tinymce.models import HTMLField

from locations.models import Location
from volunteers.models import Volunteer
from utils.image_text import draw_text_on_logo


class Campaign(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    start = models.DateField(_('Start'))
    end = models.DateField(_('End'))
    is_active = models.BooleanField(_('Is active'))
    summary = models.CharField(_('Summary'), max_length=200)
    registration_form_header = HTMLField(_('Registration form header'))
    registration_form_footer = HTMLField(_('Registration form footer'))
    registration_form_right_panel = HTMLField(_('Registration form right panel'))
    registration_confirmation_template = HTMLField(_('Registration confirmation template'))

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

    def save(self, *args, **kwargs):
        super(Campaign, self).save(*args, **kwargs)
        self._generate_card_image()

    @property
    def card_image_url(self):
        return settings.MEDIA_URL + self.card_image_name

    @property
    def card_image_name(self):
        start, end = self._start_end_in_day_month_format('j-n')
        return u'toidupank-logo-with-label-{start}-{end}.png'.format(**locals())

    @property
    def start_end_dates(self):
        start, end = self._start_end_in_day_month_format('j.n')
        return u'{start} - {end}'.format(**locals())

    def _generate_card_image(self):
        title = u'TOIDUKOGUMISPÄEVAD'
        output_filename = os.path.join(settings.MEDIA_ROOT, self.card_image_name)
        draw_text_on_logo(title, self.start_end_dates, output_filename)

    def _start_end_in_day_month_format(self, day_month_format):
        start = DateFormat(self.start)
        end = DateFormat(self.end)
        return start.format(day_month_format), end.format(day_month_format)


class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign, verbose_name=_('Campaign'))
    location = models.ForeignKey(Location, verbose_name=_('Location'))
    day = models.DateField(_('Day'))
    start = models.TimeField(_('Start'))
    end = models.TimeField(_('End'))
    total_places = models.IntegerField(_('Total places'))
    shift_leader = models.ForeignKey(Volunteer, blank=True, null=True,
            verbose_name=_('Shift leader'), related_name='shift_leader')
    volunteers = models.ManyToManyField(Volunteer, blank=True,
            verbose_name=_('Volunteers'))

    class Meta:
        unique_together = ('campaign', 'location', 'day', 'start')
        verbose_name = _('Campaign shift')
        verbose_name_plural = _('Campaign shifts')
        ordering = ['location__district__name', 'location__name', 'day', 'start']

    def __unicode__(self):
        location = unicode(self.location)
        day = date_format(self.day, 'MONTH_DAY_FORMAT')
        start = date_format(self.start, 'TIME_FORMAT')
        end = date_format(self.end, 'TIME_FORMAT')
        return u'{location} | {day}, {start}-{end} vahetus'.format(**locals())

    @property
    def detailed_info(self):
        template = u'aeg: {day}, {start}-{end}<br>koht: {location_name}, {location_address}'
        if self.shift_leader:
            shift_leader_name = self.shift_leader.name
            shift_leader_phone = self.shift_leader.phone
            template += u'<br>vahetuse vanem: {shift_leader_name}, telefon {shift_leader_phone}'
        location_name = unicode(self.location.name)
        location_address = unicode(self.location.address)
        day = date_format(self.day, 'MONTH_DAY_FORMAT')
        start = date_format(self.start, 'TIME_FORMAT')
        end = date_format(self.end, 'TIME_FORMAT')
        return format_html(template, **locals())
