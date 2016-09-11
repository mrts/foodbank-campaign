from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import signing

from .models import Volunteer


def volunteer_detail(request, key):
    data = signing.loads(key)
    volunteer = get_object_or_404(Volunteer, pk=data['pk'])
    context = {'volunteer': volunteer}
    return render(request, 'volunteers/detail.html', context)
