from django.contrib import admin
from django import forms

from campaigns.models import Campaign, CampaignLocationShift

class CampaignAdminForm(forms.ModelForm):
    def clean_is_active(self):
        is_active = self.cleaned_data['is_active']
        if is_active and Campaign.objects.filter(is_active=True).exists():
            raise forms.ValidationError('Only one campaign can be active')
        return is_active

class CampaignAdmin(admin.ModelAdmin):
    form = CampaignAdminForm
    list_display = ['name', 'start', 'end', 'is_active']
    ordering = ['-start']

class VolunteerParticipantInline(admin.TabularInline):
    model = CampaignLocationShift.volunteers.through
    verbose_name = 'Participants'
    verbose_name_plural = 'Participants'
    extra = 0
    raw_id_fields = ['volunteer']

class CampaignLocationShiftAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'location', 'day', 'start', 'end',
            'total_places', 'registered_volunteers']
    list_filter = ['campaign', 'location']
    search_fields = ['location__name', 'volunteers__name']
    date_hierarchy = 'day'
    exclude = ['volunteers']
    inlines = [VolunteerParticipantInline]

    def registered_volunteers(self, obj):
        return obj.volunteers.count()

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignLocationShift, CampaignLocationShiftAdmin)
