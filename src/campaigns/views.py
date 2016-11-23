# coding: utf-8

import json
import numbers

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseBadRequest
from django.db.models import F, Sum, IntegerField
from django.core import signing
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

from utils import string_template
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
        fields = ['group_name', 'participant_count', 'first_name',
                'last_name', 'age', 'phone', 'email', 'is_group']
        widgets = {'is_group': forms.HiddenInput()}


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
            volunteer = form.save()
            shifts = CampaignLocationShift.objects.filter(pk__in=shifts)
            volunteer.campaignlocationshift_set.add(*shifts)
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

EMAIL_TXT_TEMPLATE = u'''
Tere {{ volunteer.name }}!

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
<h2>Tere {{ volunteer.name }}!</h2>

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
