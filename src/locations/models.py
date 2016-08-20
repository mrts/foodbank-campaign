from django.db import models

class District(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


# TODO: copy-paste from kultuur.info
class Location(models.Model):
    name = models.CharField(max_length=255)

    district = models.ForeignKey(District)
    address = models.CharField(max_length=255)

    # TODO:
    # latitude = models.DecimalField()
    # longitude = models.DecimalField()

    def __unicode__(self):
        return self.name
