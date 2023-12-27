"""foodbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.utils.safestring import mark_safe

urlpatterns = [
    path('', include('campaigns.urls')),
    path(settings.ADMIN_URL_PREFIX, admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('volunteers/', include('volunteers.urls')),
    path('locations/', include('locations.urls')),
]

# from django.utils.translation import gettext_lazy as _
# _('Foodbank campaign administration') seems not to work, go figure
admin.site.site_title = 'Toidupanga kampaaniate haldamine'
admin.site.site_header = admin.site.site_title
if not settings.IS_PRODUCTION_ENV:
    admin.site.site_header = mark_safe('<span style="' +
            'background: #f00; padding: 14px; color: #fff;' +
            'font-weight: bold">TEST</span> ' + admin.site.site_header)
