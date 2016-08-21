from django.contrib import admin

from volunteers.models import Volunteer

class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'age']

admin.site.register(Volunteer, VolunteerAdmin)
