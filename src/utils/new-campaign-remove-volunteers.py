import setup_django

from volunteers.models import Volunteer

from campaigns.models import CampaignLocationShift


def count_campaignlocations(when):
    count = CampaignLocationShift.objects.count()
    print(f'Campaign locations {when} volunteers deleted: {count}')


count_campaignlocations('before')

Volunteer.objects.all().delete()

count_campaignlocations('after')

