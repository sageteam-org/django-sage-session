from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from user_session.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Session admin"""
    list_display = (
        'user', 'ip', 'location',
        'device_brand', 'device_model', 'browser',
        'os', 'is_mobile', 'is_tablet',
        'is_touch_capable', 'is_pc', 'is_valid',
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )
    readonly_fields = ('user', 'session_key')
    fieldsets = (
        (_('Security'), {
            'fields': (
                'session_key',
                'session_data',
                'expire_date',
            )
        }),
        (_('Info'), {
            'fields': (
                'user',
                'user_agent',
                'ip',
                'location',
                'device_brand',
                'device_model',
                'browser',
                'browser_version',
                'os',
                'os_version',
                'is_mobile',
                'is_tablet',
                'is_touch_capable',
                'is_pc',
                'is_bot'
            )
        })
    )

    def is_valid(self, obj):
        return obj.expire_date > now()

    is_valid.boolean = True
