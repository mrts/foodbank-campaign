from django.contrib import admin
from django.db.models import F, Sum, IntegerField
from django.utils.translation import gettext_lazy as _

import nested_admin

from .models import District, Location
from campaigns.models import CampaignLocationShift
from coordinators.models import filter_by_district

from campaigns.admin import (
    VolunteerParticipantInlineBase,
    CampaignLocationShiftForm
)

from .admin_actions import list_volunteers_by_shift_and_location

class VolunteerParticipantInline(VolunteerParticipantInlineBase, nested_admin.NestedTabularInline):
    pass

class CampaignShiftInline(nested_admin.NestedTabularInline):
    form = CampaignLocationShiftForm
    model = CampaignLocationShift
    fields = ['day', 'start', 'end', 'total_places', 'shift_leader']
    readonly_fields = ['day', 'start', 'end', 'total_places']
    exclude = ['volunteers']
    inlines = [VolunteerParticipantInline]
    extra = 0


class LocationAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['name', 'address',
            'campaignlocationshift__volunteers__first_name',
            'campaignlocationshift__volunteers__last_name']
    list_filter = ['district']
    inlines = [CampaignShiftInline]
    list_display = ['name', 'volunteers_count', 'free_places']
    save_on_top = True
    actions = [list_volunteers_by_shift_and_location]

    def volunteers_count(self, obj):
        return obj.campaignlocationshift_set.aggregate(
                count=Sum('volunteers__participant_count'))['count']
    volunteers_count.short_description = _('Volunteers count')

    def free_places(self, obj):
        total_places = obj.campaignlocationshift_set.aggregate(total=Sum(
            'total_places'))['total']
        taken_places = obj.campaignlocationshift_set.aggregate(taken=Sum(
            'volunteers__participant_count'))['taken']
        return int(total_places or 0) - int(taken_places or 0)
    free_places.short_description = _('Free places')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_district(qs, request.user, 'district')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(District)
admin.site.register(Location, LocationAdmin)
