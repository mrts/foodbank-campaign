from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from volunteers.models import Volunteer, ShiftLeader
from coordinators.models import filter_by_district
from campaigns.admin import VolunteerParticipantInline


class CampaignLocationShiftInline(VolunteerParticipantInline):
    verbose_name = _('Campaign shift')
    verbose_name_plural = _('Campaign shifts')
    raw_id_fields = ['campaignlocationshift']
    # get_queryset is inherited from VolunteerParticipantInline,
    # but filtering seems to fail...


class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'age',
            'is_group', 'participant_count']
    fieldsets = [
            (None, {'fields': ('first_name', 'last_name', 'age', 'phone',
                'email', 'notes')}),
            (_('Group'), {'fields': ('is_group', 'group_name', 'participant_count')})
    ]
    inlines = [CampaignLocationShiftInline]

    def get_queryset(self, request):
        qs = super(VolunteerAdmin, self).get_queryset(request)
        return filter_by_district(qs, request.user,
                'campaignlocationshift__location__district')


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(ShiftLeader)
