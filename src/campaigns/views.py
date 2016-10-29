import json
import numbers

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseBadRequest
from django.db.models import F, Sum, IntegerField
from django.core import signing
from django.utils.translation import ugettext as _

from campaigns.models import Campaign, CampaignLocationShift
from volunteers.models import Volunteer
from locations.models import District


class VolunteerRegistrationForm(forms.ModelForm):
    selected_shifts = forms.CharField(widget = forms.HiddenInput())

    # add Bootstrap classes
    def __init__(self, *args, **kwargs):
        super(VolunteerRegistrationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Volunteer
        fields = '__all__' # TODO: careful with this
        widgets = {'is_group': forms.HiddenInput()}


def registration(request):
    if request.method == 'POST' and request.POST:
        form = VolunteerRegistrationForm(request.POST)
        form_is_valid = form.is_valid()
        try:
            shifts = request.POST['selected_shifts']
            shifts = json.loads(shifts) if shifts else []
            for shift in shifts:
                if not isinstance(shift, numbers.Integral):
                    raise ValueError()
        except ValueError:
            return HttpResponseBadRequest('Invalid shifts in POST data')
        if not shifts:
            form.add_error(None, _('No shift selected'))
        elif form_is_valid:
            # FIXME: try to fetch by email and name first?
            # or use UpdateView altogether
            volunteer = form.save()
            shifts = CampaignLocationShift.objects.filter(pk__in=shifts)
            volunteer.campaignlocationshift_set.add(*shifts)
            volunteer_key = signing.dumps({
                'email': volunteer.email,
                'pk': volunteer.pk,
            })
            volunteer_detail_url = reverse('volunteer_detail',
                    kwargs={'key': volunteer_key})
            return redirect(volunteer_detail_url)
    else:
        form = VolunteerRegistrationForm()
    try:
        campaign = Campaign.objects.get(is_active=True)
        districts = (District.objects
                .filter(location__campaignlocationshift__campaign=campaign)
                .order_by('name')
                .distinct())
        # TODO: refactor annotate() to custom manager
        locations_and_shifts = (CampaignLocationShift.objects
                .filter(campaign=campaign)
                .annotate(free_places=F('total_places') -
                                      Sum('volunteers__participant_count',
                                          output_field=IntegerField())))
        context = {
            'campaign': campaign,
            'districts': list(districts),
            'locations_and_shifts': list(locations_and_shifts),
            'form': form,
        }
        return render(request, 'campaigns/registration.html', context)
    except Campaign.DoesNotExist:
        return render(request, 'campaigns/no-active-campaign.html')
