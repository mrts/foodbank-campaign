from django.db import models
from django.forms.widgets import Textarea
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from volunteers.models import Volunteer
from coordinators.models import filter_by_district
from campaigns.admin import VolunteerParticipantInline


class CampaignLocationShiftInline(VolunteerParticipantInline):
    verbose_name = _('Campaign shift')
    verbose_name_plural = _('Campaign shifts')
    raw_id_fields = ['shift']
    # get_queryset is inherited from VolunteerParticipantInline,
    # but filtering seems to fail...


class VolunteerAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'age',
            'is_group', 'participant_count']
    readonly_fields = ['registration_time']
    fieldsets = [
            (None, {'fields': ('first_name', 'last_name', 'age', 'phone',
                'email', 'notes', 'public_notes')}),
            (_('Group'), {'fields': ('is_group', 'group_name',
                'participant_count')}),
            (_('Districts'), {'fields': ('districts',)}),
            (_('Registration details'), {
                'fields': ('registration_time',
                    'registration_ip_address','registration_user_agent'),
                'classes': ('collapse',),
            }),
    ]
    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={
                'rows': '2',
                'cols': '40',
            })},
    }
    inlines = [CampaignLocationShiftInline]

    def get_queryset(self, request):
        qs = super(VolunteerAdmin, self).get_queryset(request)
        return filter_by_district(qs, request.user, 'districts')



admin.site.register(Volunteer, VolunteerAdmin)
