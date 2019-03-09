import sys

import setup_django

from utils.dateutils import get_first_second_day_from_arg

from campaigns.models import Campaign

new_first_day, new_second_day = get_first_second_day_from_arg(sys.argv[1])

campaign = Campaign.objects.get()

season = 'Talv' if new_first_day.month > 10 else 'Kevad'

campaign.name = f'{season}ine toidukogumiskampaania'
campaign.start = new_first_day
campaign.end = new_second_day
campaign.is_active = True
campaign.save()
