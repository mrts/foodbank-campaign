from django.contrib import admin

from locations.models import District, Location

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'address']
    list_filter = ['district']

admin.site.register(District)
admin.site.register(Location, LocationAdmin)
