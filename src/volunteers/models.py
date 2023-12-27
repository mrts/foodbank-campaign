from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from locations.models import District


class Volunteer(models.Model):
    group_name = models.CharField(_('Group/organization name'), max_length=100,
            blank=True)
    participant_count = models.PositiveIntegerField(_('Participant count'),
            default=1, validators=[MinValueValidator(1)])
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    age = models.PositiveIntegerField(_('Age'), blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=100)
    email = models.EmailField(_('E-mail'))
    is_group = models.BooleanField(_('Is group representative'), default=False)
    notes = models.TextField(_('Notes'), blank=True)
    public_notes = models.TextField(_('Public notes'), blank=True)
    districts = models.ManyToManyField(District, blank=True,
            verbose_name=_('Districts'))
    registration_time = models.DateTimeField(_('Registration time'),
            auto_now_add=True, db_index=True)
    registration_ip_address = models.GenericIPAddressField(
            _('Registration IP address'), db_index=True, blank=True, null=True)
    registration_user_agent = models.CharField(_('Registration user agent'),
            max_length=255, blank=True)

    class Meta:
        verbose_name = _('Volunteer')
        verbose_name_plural = _('Volunteers')
        unique_together = ['email', 'group_name', 'first_name', 'last_name']
        index_together = unique_together

    @property
    def name(self):
        template = u'{first_name} {last_name}'
        if self.is_group:
            template += u' ({group_name} grupp, {participant_count} osalejat)'
        return template.format(**self.__dict__)

    @property
    def shifts(self):
        return self.campaignlocationshift_set.order_by('day', 'start')

    def __str__(self):
        return self.name
