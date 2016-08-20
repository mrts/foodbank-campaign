from django.shortcuts import render
from django import forms
from django.db.models import Count, F

from campaigns.models import Campaign, CampaignLocationShift
from volunteers.models import Volunteer
from locations.models import District


class VolunteerRegistrationForm(forms.ModelForm):
    # add Bootstrap classes
    def __init__(self, *args, **kwargs):
        super(VolunteerRegistrationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Volunteer
        fields = '__all__' # TODO: careful with this


def registration(request):
    try:
        campaign = Campaign.objects.get(is_active=True)
        districts = District.objects.filter(
                location__campaignlocationshift__isnull=False).order_by('name').distinct()
        locations_and_shifts = CampaignLocationShift.objects.filter(
                campaign=campaign).annotate(free_places=F('total_places') - Count('volunteers'))
        context = {
            'campaign': campaign,
            'districts': districts,
            'locations_and_shifts': locations_and_shifts,
            'form': VolunteerRegistrationForm(),
        }
        return render(request, 'campaigns/registration.html', context)
    except Campaign.DoesNotExist:
        return render(request, 'campaigns/no-active-campaign.html')
