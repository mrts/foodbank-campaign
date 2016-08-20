from django.contrib import admin

from volunteers.models import Volunteer

class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Volunteer, VolunteerAdmin)
