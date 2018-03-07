from django.contrib import admin

from system import models


class AccessLogsAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'create_at', 'routing', 'ip_address', 'browser', 'system')
    search_fields = (
        'username', 'create_at', 'routing', 'ip_address', 'browser', 'system')


admin.site.register(models.AccessLogs, AccessLogsAdmin)