import sys

import setup_django

from utils.dateutils import get_first_second_day_from_arg

from campaigns.models import CampaignLocationShift

def update_shifts(shifts, day):
    for shift in shifts:
        shift.day = day
        shift.save()

old_first_day, old_second_day = get_first_second_day_from_arg(sys.argv[1])
new_first_day, new_second_day = get_first_second_day_from_arg(sys.argv[2])

first_day_shifts = CampaignLocationShift.objects.filter(day=old_first_day)
second_day_shifts = CampaignLocationShift.objects.filter(day=old_second_day)
print(f'First day shifs count: {len(first_day_shifts)}')
print(f'Second day shifs count: {len(second_day_shifts)}')

update_shifts(first_day_shifts, new_first_day)
update_shifts(second_day_shifts, new_second_day)

