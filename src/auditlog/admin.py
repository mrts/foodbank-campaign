from django.contrib import admin

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = [field.name for field in LogEntry._meta.get_fields()]
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]
    search_fields = [
        'object_repr',
        'change_message'
    ]
    list_display = [
        '__str__',
        'action_time',
        'user',
        'content_type',
        'object_link',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # cannot return False, the module wouldn't be visible in admin
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            ))
        return link
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')
