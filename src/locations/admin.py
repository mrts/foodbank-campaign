from django.contrib import admin

import nested_admin

from locations.models import District, Location
from campaigns.models import CampaignLocationShift
from campaigns.admin import VolunteerParticipantInline


class CampaignShiftInline(nested_admin.NestedTabularInline):
    model = CampaignLocationShift
    exclude = ['volunteers']
    inlines = [VolunteerParticipantInline]
    extra = 0


class LocationAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['name', 'address']
    list_filter = ['district']
    inlines = [CampaignShiftInline]


admin.site.register(District)
admin.site.register(Location, LocationAdmin)
