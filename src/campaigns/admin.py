from django.contrib import admin

from campaigns.models import Campaign, CampaignLocationShift


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'is_active']
    ordering = ['-is_active', '-start']


class VolunteerParticipantInline(admin.TabularInline):
    model = CampaignLocationShift.volunteers.through
    verbose_name = 'Participants'
    verbose_name_plural = 'Participants'
    extra = 0
    raw_id_fields = ['volunteer']

    class Media:
        js = ['campaigns/make-volunteer-readonly.js']


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
