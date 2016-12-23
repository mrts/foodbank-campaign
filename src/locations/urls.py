from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^overview/$', views.overview, name='overview'),
]
