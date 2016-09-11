from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<key>[-:\w]+)/$', views.volunteer_detail, name='volunteer_detail'),
]
