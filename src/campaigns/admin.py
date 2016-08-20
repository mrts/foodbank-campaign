from django.contrib import admin

from campaigns.models import (Campaign, CampaignLocationShift,
        CampaignLocationShiftVolunteers)

admin.site.register(Campaign)
admin.site.register(CampaignLocationShift)
admin.site.register(CampaignLocationShiftVolunteers)
