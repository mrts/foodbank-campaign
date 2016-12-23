from collections import namedtuple

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from .models import Location

LocationSummary = namedtuple('LocationSummary', ['name', 'leaders', 'volunteers'])

@user_passes_test(lambda u: u.is_superuser)
def overview(request):
    locations = Location.objects.all()
    result = []
    for location in locations.order_by('district'):
        locationsummary = LocationSummary(location.name, set(), set())
        for shift in location.campaignlocationshift_set.all():
            if shift.shift_leader:
                locationsummary.leaders.add(shift.shift_leader)
            for participation in shift.campaignlocationshiftparticipation_set.all():
                locationsummary.volunteers.add(participation.volunteer)
        result.append(locationsummary)
    return render(request, 'locations/overview.html', {'locations': result})
