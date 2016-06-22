from django.db import models

class LocationContact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    skype = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


# TODO: copy-paste from kultuur.info
class Location(models.Model):
    name = models.CharField(max_length=255)
    contacts = models.ManyToManyField(LocationContact)

    district = models.ForeignKey(District)
    address = models.CharField(max_length=255)

    # TODO:
    # latitude = models.DecimalField()
    # longitude = models.DecimalField()

    def __unicode__(self):
        return self.name
