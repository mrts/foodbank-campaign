from django.db import models

from locations.models import Location
from volunteers.models import Volunteer


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        unique_together = ('start', 'name')

    def __unicode__(self):
        return u"{start} {name} kampaania".format(**self.__dict__)

class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign)
    location = models.ForeignKey(Location)
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __unicode__(self):
        campaign = unicode(self.campaign)
        location = unicode(self.location)
        day = unicode(self.day)
        start = unicode(self.start)
        end = unicode(self.end)
        return u"{campaign} {location} {day} {start}-{end} vahetus".format(**locals())

class CampaignLocationShiftVolunteers(models.Model):
    campaign_location_shift = models.ForeignKey(CampaignLocationShift)
    volunteers = models.ManyToManyField(Volunteer)

    class Meta:
        verbose_name_plural = 'Campaing location shift volunteers'

    def __unicode__(self):
        campaign_location_shift = unicode(self.campaign_location_shift)
        count = self.volunteers.count()
        return u"{campaign_location_shift}: {count} osalejat".format(**locals())
