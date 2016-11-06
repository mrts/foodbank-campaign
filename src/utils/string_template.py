import string

from django.template import engines

def render_django_template(template, request, context):
    template = engines['django'].from_string(template)
    return template.render(context, request)

def render_campaign_registration_template(template, campaign, request, context):
    template = string.Template(template)
    template = template.substitute({
        'content': campaign.registration_confirmation_template
    })
    return render_django_template(template, request, context)
