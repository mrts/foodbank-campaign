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
            and 'group_name' in request.POST):
        volunteer = Volunteer.objects.filter(email=request.POST['email'],
                group_name=request.POST['group_name'])
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
            # FIXME: try to fetch by email and name first?
            # or use UpdateView altogether
            volunteer = form.save()
            shifts = CampaignLocationShift.objects.filter(pk__in=shifts)
            volunteer.campaignlocationshift_set.add(*shifts)
            volunteer_key = signing.dumps({
                'group_name': volunteer.group_name,
                'email': volunteer.email,
                'pk': volunteer.pk,
            })
            volunteer_detail_url = reverse('volunteer_detail',
                    kwargs={'key': volunteer_key})
            campaign = Campaign.objects.get(is_active=True)
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

EMAIL_TEMPLATE = '''{% extends "campaigns/base.html" %}
{% block title %}Tere {{ volunteer.name }}!{% endblock title %}

{% block body %}

<div class="container">

  <div class="row">
    <div class="col-md-12">
      <div class="page-header">
        <h1>Tere {{ volunteer.name }}!</h1>
      </div>
      <p>Link <a href="{{ volunteer_detail_url }}">registreerumisinfole</a>.</p>
      ${content}
    </div>
  </div>

</div> <!-- container -->
{% endblock body %}
'''
def _send_confirmation_email(request, campaign, volunteer,
        volunteer_detail_url):
    context = {
        'volunteer': volunteer,
        'volunteer_detail_url': volunteer_detail_url
    }
    content = string_template.render(EMAIL_TEMPLATE, campaign, request, context)
    send_mail(u'Toidukogumispäeva info vabatahtlikule',
              u'Info on sõnumile lisatud HTML-formaadis',
              'info@toidupank.ee', [volunteer.email],
              fail_silently=False, html_message=content)
