import setup_django

from campaigns.models import CampaignLocationShift

shifts = list(CampaignLocationShift.objects
              .exclude(shift_leader=None)
              .order_by('location__name'))

leaders = '\n'.join(sorted(set(f'{shift.location}: {shift.shift_leader.name}, '
                               f'{shift.shift_leader.email}, tel. {shift.shift_leader.phone}'
                               for shift in shifts)))

with open('shift-leaders.txt', 'w', encoding='utf-8') as output:
    output.write(leaders)

for shift in shifts:
    shift.shift_leader = None
    shift.save()
