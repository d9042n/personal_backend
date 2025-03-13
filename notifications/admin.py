"""
Django admin configuration for the notifications app.

This module configures how notification models are displayed and managed
in the Django admin interface.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import logging

from .models import Notification

logger = logging.getLogger(__name__)


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
        logger.debug("Attempted manual notification creation in admin interface")
        return False

    def save_model(self, request, obj, form, change):
        """
        Log notification changes made through admin interface.
        
        Args:
            request: The HTTP request
            obj: The notification instance being saved
            form: The form instance
            change: Boolean indicating if this is an update
        """
        try:
            action = "updated" if change else "created"
            logger.info(
                f"Admin {request.user.username} {action} notification {obj.id} "
                f"for user {obj.recipient.username}"
            )
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(
                f"Error saving notification {obj.id} in admin interface: {str(e)}",
                exc_info=True
            )
            raise

    def delete_model(self, request, obj):
        """
        Log notification deletion through admin interface.
        
        Args:
            request: The HTTP request
            obj: The notification instance being deleted
        """
        try:
            logger.info(
                f"Admin {request.user.username} deleted notification {obj.id} "
                f"for user {obj.recipient.username}"
            )
            super().delete_model(request, obj)
        except Exception as e:
            logger.error(
                f"Error deleting notification {obj.id} in admin interface: {str(e)}",
                exc_info=True
            )
            raise

    def delete_queryset(self, request, queryset):
        """
        Log bulk notification deletion through admin interface.
        
        Args:
            request: The HTTP request
            queryset: The queryset of notifications being deleted
        """
        try:
            count = queryset.count()
            notification_ids = list(queryset.values_list('id', flat=True))
            logger.info(
                f"Admin {request.user.username} bulk deleted {count} notifications: "
                f"IDs {notification_ids}"
            )
            super().delete_queryset(request, queryset)
        except Exception as e:
            logger.error(
                f"Error bulk deleting notifications in admin interface: {str(e)}",
                exc_info=True
            )
            raise
