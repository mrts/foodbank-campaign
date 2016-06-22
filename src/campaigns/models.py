from django.db import models

from locations.models import Location
from volunteers.models import Volunteer


class Campaign(models.Model):
    start = models.DateField()
    end = models.DateField()
    name = models.CharField(max_length=255)
    locations = models.ManyToManyField(Location)

    class Meta:
        unique_together = ('start', 'name')

    def __unicode__(self):
        return u"{start} {name} kampaania".format(**self.__dict__)

class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign)
    location = models.ForeignKey(Location)
    volunteers = models.ManyToManyField(Volunteer)
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
