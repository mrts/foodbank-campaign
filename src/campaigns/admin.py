# coding: utf-8

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


class VolunteerParticipantInlineBase:
    model = CampaignLocationShiftParticipation
    verbose_name = _('Participant')
    verbose_name_plural = _('Participants')
    extra = 0
    autocomplete_fields = ['volunteer']
    readonly_fields = ['volunteer_details']
    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={
                'rows': '2',
                'cols': '40',
            })},
    }
    # TODO: need to implement get_queryset to limit shifts by location

    def volunteer_details(self, instance):
        volunteer = instance.volunteer
        template = u'tel: {phone}, email: {email}, vanus: {age}'
        if volunteer.public_notes:
            template += u', avalikud märkmed: {public_notes}'
        return template.format(**volunteer.__dict__)
    volunteer_details.short_description = _('Volunteer details')


class VolunteerParticipantInline(VolunteerParticipantInlineBase, admin.TabularInline):
    pass


class CampaignLocationShiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        qs = super().get_queryset(request)
        return filter_by_district(qs, request.user, 'location__district')


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignLocationShift, CampaignLocationShiftAdmin)
