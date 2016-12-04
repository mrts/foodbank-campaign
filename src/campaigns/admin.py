from django import forms
from django.forms.widgets import Textarea
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Sum

import nested_admin

from campaigns.models import (
    Campaign,
    CampaignLocationShift,
    CampaignLocationShiftParticipation
)
from coordinators.models import filter_by_district
from volunteers.models import Volunteer


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'is_active']
    ordering = ['-is_active', '-start']


class VolunteerParticipantInline(nested_admin.NestedTabularInline):
    model = CampaignLocationShiftParticipation
    verbose_name = _('Participant')
    verbose_name_plural = _('Participants')
    extra = 0
    raw_id_fields = ['volunteer']
    show_change_link = True
    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={
                'rows': '2',
                'cols': '40',
            })},
    }

    class Media:
        # js = ['campaigns/js/make-rawid-readonly.js']
        css = {'all': ['campaigns/css/hide-rawid.css']}


class CampaignLocationShiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignLocationShiftForm, self).__init__(*args, **kwargs)
        self.fields['shift_leader'].queryset = Volunteer.objects.filter(campaignlocationshift=self.instance)


class CampaignLocationShiftAdmin(admin.ModelAdmin):
    form = CampaignLocationShiftForm
    list_display = ['location', 'day', 'start', 'end',
            'total_places', 'registered_volunteers']
    list_filter = ['campaign', 'location']
    search_fields = ['location__name',
                     'volunteers__first_name',
                     'volunteers__last_name',
                     'volunteers__group_name']
    date_hierarchy = 'day'
    exclude = ['volunteers']
    inlines = [VolunteerParticipantInline]

    def registered_volunteers(self, obj):
        count = obj.volunteers.aggregate(participants=Sum('participant_count'))
        return count['participants']
    registered_volunteers.short_description = _('Registered volunteers')

    def get_queryset(self, request):
        qs = super(CampaignLocationShiftAdmin, self).get_queryset(request)
        return filter_by_district(qs, request.user, 'location__district')


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignLocationShift, CampaignLocationShiftAdmin)
