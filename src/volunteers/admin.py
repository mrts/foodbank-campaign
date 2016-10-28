from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from campaigns.admin import VolunteerParticipantInline
from volunteers.models import Volunteer

class CampaignLocationShiftInline(VolunteerParticipantInline):
    verbose_name = _('Campaign shift')
    verbose_name_plural = _('Campaign shifts')
    raw_id_fields = ['campaignlocationshift']

class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'age',
            'is_group', 'participant_count']
    fieldsets = [
            (None, {'fields': ('first_name', 'last_name', 'age', 'phone',
                'email')}),
            (_('Group'), {'fields': ('is_group', 'group_name', 'participant_count')})
    ]
    inlines = [CampaignLocationShiftInline]

admin.site.register(Volunteer, VolunteerAdmin)
