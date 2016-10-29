# coding: utf-8

import string

from django.shortcuts import get_object_or_404
from django.template import engines
from django.http import HttpResponse
from django.core import signing

from campaigns.models import Campaign, CampaignLocationShift
from .models import Volunteer


TEMPLATE = '''{% extends "campaigns/base.html" %}
{% block title %}Tere {{ volunteer.name }}!{% endblock title %}

{% block body %}

<div class="container">

  <div class="row">
    <div class="col-md-12">
      <div class="page-header">
        <h1>Tere {{ volunteer.name }}!</h1>
      </div>
      ${content}
    </div>
  </div>

</div> <!-- container -->
{% endblock body %}
'''

dummy='''
      <p>Olete registreerunud järgmistele vahetustele:</p>
      <ol>
        {% for shift in volunteer.campaignlocationshift_set.all %}
        <li>{{ shift }}</li>
        {% endfor %}
      </ol>
'''

def volunteer_detail(request, key):
    try:
        campaign = Campaign.objects.get(is_active=True)
    except Campaign.DoesNotExist:
        return render(request, 'campaigns/no-active-campaign.html')

    data = signing.loads(key)
    volunteer = get_object_or_404(Volunteer, pk=data['pk'])
    context = {'volunteer': volunteer}

    template = string.Template(TEMPLATE)
    template = template.substitute({
        'content': campaign.registration_confirmation_template
    })
    template = engines['django'].from_string(template)
    content = template.render(context, request)

    return HttpResponse(content)
