# coding: utf-8

import json
import numbers

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.http import HttpResponseBadRequest
from django.core import signing
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

from utils import string_template
from utils.request import get_ip_address, get_user_agent
from campaigns.models import (
    Campaign, CampaignLocationShift, CampaignLocationShiftParticipation
)
from volunteers.models import Volunteer
from locations.models import District


class VolunteerRegistrationForm(forms.ModelForm):
    selected_shifts = forms.CharField(widget = forms.HiddenInput())

    class Meta:
        model = Volunteer
        fields = ['group_name', 'participant_count', 'first_name',
                'last_name', 'age', 'phone', 'email', 'is_group']
        widgets = {'is_group': forms.HiddenInput()}

    # add Bootstrap classes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_valid():
            return
        is_group = cleaned_data.get('is_group')
        if not is_group:
            cleaned_data['participant_count'] = 1


def registration(request):
    if (request.method == 'POST' and request.POST
            and 'email' in request.POST and request.POST['email'].strip()
            and 'group_name' in request.POST
            and 'first_name' in request.POST
            and 'last_name' in request.POST):
        volunteer = Volunteer.objects.filter(email=request.POST['email'],
                group_name=request.POST['group_name'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'])
        form = (VolunteerRegistrationForm(request.POST) if not volunteer else
                VolunteerRegistrationForm(request.POST, instance=volunteer[0]))
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
            volunteer = form.save(commit=False)
            volunteer.registration_ip_address = get_ip_address(request)
            volunteer.registration_user_agent = get_user_agent(request)
            volunteer.save()
            shifts = CampaignLocationShift.objects.filter(pk__in=shifts)
            for shift in shifts:
                CampaignLocationShiftParticipation.objects.update_or_create(
                        shift=shift, volunteer=volunteer)
            volunteer_key = signing.dumps({
                'email': volunteer.email,
                'pk': volunteer.pk,
            })
            volunteer_detail_url = request.build_absolute_uri(
                    reverse('volunteer_detail',
                        kwargs={'key': volunteer_key}))
            campaign = Campaign.objects.get(is_active=True)
            # TODO: prefetch related, use Django Debug Toolbar to debug
            _send_confirmation_email(request, campaign, volunteer,
                    volunteer_detail_url)
            return redirect(volunteer_detail_url)
    else:
        form = VolunteerRegistrationForm()
    try:
        campaign = Campaign.objects.get(is_active=True)
        districts = (District.objects
                .filter(location__campaignlocationshift__campaign=campaign)
                .order_by('name')
                .distinct())
        locations_and_shifts = (CampaignLocationShift.objects
                .with_free_places()
                .filter(campaign=campaign))
        context = {
            'campaign': campaign,
            'districts': list(districts),
            'locations_and_shifts': list(locations_and_shifts),
            'form': form,
            'is_test_env': not settings.IS_PRODUCTION_ENV,
        }
        return render(request, 'campaigns/registration.html', context)
    except Campaign.DoesNotExist:
        return render(request, 'campaigns/no-active-campaign.html')

EMAIL_TXT_TEMPLATE = u'''
Tere, {{ volunteer.name }}!

Oled registreerunud Toidupanga toidukogumispävadele järgmistele vahetustele:

{% for shift in volunteer.shifts %}
* {{ shift.detailed_info }}
{% endfor %}

Täpsem info on sõnumile lisatud HTML-formaadis ning veebis saadaval
alljärgnevalt lingilt:

{{ volunteer_detail_url }}

Kohtumiseni toidukogumispäevadel!

Tänades,
Toidupanga meeskond
'''

EMAIL_HTML_TEMPLATE = u'''<html>
<body>
<h2>Tere, {{ volunteer.name }}!</h2>

<p>Valitud vahetused:</p>
{% for shift in volunteer.shifts %}
<ul>
<li><b>{{ shift.detailed_info }}</b></li>
</ul>
{% endfor %}

<p>Registreerumisinfo on saadaval ka <a href="{{ volunteer_detail_url }}">veebis</a>.</p>

${content}

</body>
</html>
'''
def _send_confirmation_email(request, campaign, volunteer,
        volunteer_detail_url):
    context = {
        'volunteer': volunteer,
        'volunteer_detail_url': volunteer_detail_url
    }
    txt_message = string_template.render_django_template(EMAIL_TXT_TEMPLATE,
            request, context)
    html_message = string_template.render_campaign_registration_template(
            EMAIL_HTML_TEMPLATE, campaign, request, context)
    send_mail(u'Toidukogumispäeva info vabatahtlikule',
              txt_message, 'info@toidupank.ee', [volunteer.email],
              fail_silently=False, html_message=html_message)
