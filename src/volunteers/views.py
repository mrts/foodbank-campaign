# coding: utf-8

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import signing

from utils import string_template
from campaigns.models import Campaign, CampaignLocationShift
from .models import Volunteer


TEMPLATE = u'''{% extends "campaigns/base.html" %}
{% block title %}Tere {{ volunteer.name }}!{% endblock title %}

{% block header %}
        <h1>Tere {{ volunteer.name }}!</h1>
{% endblock header %}

{% block content %}
    <div class="col-md-12">
      <p>Valitud vahetused:</p>
        {% for shift in volunteer.shifts %}
        <ul>
        <li><b>{{ shift.detailed_info }}</b></li>
        </ul>
        {% endfor %}
      <p>Käesolev info on saadetud ka sisestatud meiliaadressile.</p>
      ${content}
    </div>
{% endblock content %}
'''

def volunteer_detail(request, key):
    try:
        campaign = Campaign.objects.get(is_active=True)
    except Campaign.DoesNotExist:
        return render(request, 'campaigns/no-active-campaign.html')

    data = signing.loads(key)
    volunteer = get_object_or_404(Volunteer, pk=data['pk'])

    context = {'volunteer': volunteer}
    content = string_template.render_campaign_registration_template(TEMPLATE,
            campaign, request, context)

    return HttpResponse(content)
