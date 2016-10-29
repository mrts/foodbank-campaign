import string

from django.template import engines


def render(template, campaign, request, context):
    template = string.Template(template)
    template = template.substitute({
        'content': campaign.registration_confirmation_template
    })
    template = engines['django'].from_string(template)
    content = template.render(context, request)
    return content
