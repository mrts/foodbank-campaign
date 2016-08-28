from django.db import models
from django.core.exceptions import ValidationError

from tinymce.models import HTMLField

from locations.models import Location
from volunteers.models import Volunteer


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField()
    registration_form_header = HTMLField()
    registration_form_footer = HTMLField()
    registration_form_right_panel = HTMLField()

    class Meta:
        unique_together = ('start', 'name')

    def __unicode__(self):
        return u"{start} {name}".format(**self.__dict__)

    def clean(self):
        if (self.is_active and Campaign.objects
                .filter(is_active=True)
                .exclude(pk=self.pk) # works when pk is None, too
                .exists()):
            raise ValidationError('Only one campaign can be active at a time')


class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign)
    location = models.ForeignKey(Location)
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    total_places = models.IntegerField()
    volunteers = models.ManyToManyField(Volunteer, blank=True)

    class Meta:
        unique_together = ('campaign', 'location', 'day', 'start')

    def __unicode__(self):
        campaign = unicode(self.campaign)
        location = unicode(self.location)
        day = unicode(self.day)
        start = unicode(self.start)
        end = unicode(self.end)
        return u"{campaign} {location} {day} {start}-{end} vahetus".format(**locals())
