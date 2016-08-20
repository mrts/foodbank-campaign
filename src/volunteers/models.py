from django.db import models

class Volunteer(models.Model):
    first_name = models.CharField('Eesnimi', max_length=100)
    last_name = models.CharField('Perenimi', max_length=100)
    age = models.PositiveIntegerField('Vanus')
    phone = models.CharField('Telefon', max_length=100)
    email = models.EmailField('E-mail', unique=True)

    @property
    def name(self):
        return "{first_name} {last_name}".format(**self.__dict__)

    def __unicode__(self):
        return self.name
