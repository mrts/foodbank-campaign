from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

def list_volunteers_by_shift_and_location(modeladmin, request, queryset):
    return render(request,
            'locations/list_volunteers_by_shift_and_location.html',
            context = {'locations': queryset})
list_volunteers_by_shift_and_location.short_description = _('List of volunteers by location and shift')
