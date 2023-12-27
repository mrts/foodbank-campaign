from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from coordinators.models import Coordinator

class CoordinatorInline(admin.StackedInline):
    model = Coordinator
    can_delete = False
    verbose_name_plural = _('coordinator')

class UserAdmin(BaseUserAdmin):
    inlines = (CoordinatorInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
