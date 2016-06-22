from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # TODO: need back reference here for the many-to-many in shifts

    def __unicode__(self):
        return self.name
