from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'(?P<key>[-:\w]+)/', views.volunteer_detail, name='volunteer_detail'),
]
