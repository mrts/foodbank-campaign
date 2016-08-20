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
        return u"{start} {name}".format(**self.__dict__)

class CampaignLocationShift(models.Model):
    campaign = models.ForeignKey(Campaign)
    location = models.ForeignKey(Location)
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    total_places = models.IntegerField()
    volunteers = models.ManyToManyField(Volunteer, null=True, blank=True)

    class Meta:
        unique_together = ('campaign', 'location', 'day', 'start')

    def __unicode__(self):
        campaign = unicode(self.campaign)
        location = unicode(self.location)
        day = unicode(self.day)
        start = unicode(self.start)
        end = unicode(self.end)
        return u"{campaign} {location} {day} {start}-{end} vahetus".format(**locals())
