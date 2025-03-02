"""
Django admin configuration for the notifications app.

This module configures how notification models are displayed and managed
in the Django admin interface.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    
    This class customizes how notifications are displayed and managed in the
    Django admin interface, including list views, filters, and search capabilities.
    """
    
    list_display = (
        'recipient',
        'notification_type',
        'message',
        'is_read',
        'created_at'
    )
    list_filter = (
        'notification_type',
        'is_read',
        'created_at'
    )
    search_fields = (
        'recipient__username',
        'actor__username',
        'message'
    )
    readonly_fields = (
        'created_at',
        'updated_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': (
                'recipient',
                'actor',
                'notification_type',
                'message'
            )
        }),
        (_('Content'), {
            'fields': (
                'content_type',
                'object_id',
                'data'
            )
        }),
        (_('Status'), {
            'fields': (
                'is_read',
                'is_deleted'
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        """
        Disable manual notification creation in admin.
        
        Notifications should only be created through the API or signals.
        """
        return False
