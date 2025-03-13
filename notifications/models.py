from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
import logging

from .constants import NotificationTypes

logger = logging.getLogger(__name__)


class Notification(models.Model):
    """
    Model to handle system notifications for users.
    
    This model stores notifications that can be triggered by various system events,
    user actions, or automated processes. It supports generic relations to allow
    notifications to reference any model object.
    
    Attributes:
        recipient: User who will receive the notification
        actor: User who triggered the notification (optional)
        content_type: Type of the related object for generic relation
        object_id: ID of the related object for generic relation
        content_object: The actual related object (GenericForeignKey)
        notification_type: Type of notification (from NotificationTypes)
        message: The notification message
        data: Additional JSON data for the notification
        is_read: Whether the notification has been read
        is_deleted: Soft deletion status
        created_at: When the notification was created
        updated_at: When the notification was last updated
    """
    # Core fields
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Recipient'),
        help_text=_('User who will receive the notification')
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_notifications',
        verbose_name=_('Actor'),
        help_text=_('User who triggered the notification')
    )

    # Generic relation fields
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Content Type'),
        help_text=_('Type of the related object')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID'),
        help_text=_('ID of the related object')
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Notification details
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationTypes.CHOICES,
        verbose_name=_('Type'),
        help_text=_('Type of notification')
    )

    message = models.TextField(
        verbose_name=_('Message'),
        help_text=_('Notification message text')
    )

    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Additional Data'),
        help_text=_('Additional JSON data for the notification')
    )

    # Status fields
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Read Status'),
        help_text=_('Whether the notification has been read')
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_('Deleted Status'),
        help_text=_('Soft deletion status')
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At'),
        help_text=_('When the notification was created')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At'),
        help_text=_('When the notification was last updated')
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
        ]
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:50]}"

    def save(self, *args, **kwargs):
        """Override save to add logging"""
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new:
            logger.info(
                f"Created notification {self.id} of type {self.notification_type} "
                f"for recipient {self.recipient.username}"
            )
            if self.actor:
                logger.debug(f"Notification {self.id} triggered by user {self.actor.username}")
        else:
            logger.debug(f"Updated notification {self.id} for recipient {self.recipient.username}")

    def mark_as_read(self):
        """Mark the notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read', 'updated_at'])
            logger.info(f"Notification {self.id} marked as read by recipient {self.recipient.username}")

    def mark_as_unread(self):
        """Mark the notification as unread"""
        if self.is_read:
            self.is_read = False
            self.save(update_fields=['is_read', 'updated_at'])
            logger.info(f"Notification {self.id} marked as unread by recipient {self.recipient.username}")

    def soft_delete(self):
        """Soft delete the notification"""
        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=['is_deleted', 'updated_at'])
            logger.info(f"Notification {self.id} soft deleted for recipient {self.recipient.username}")

    def delete(self, *args, **kwargs):
        """Override delete to add logging"""
        logger.info(f"Permanently deleting notification {self.id} for recipient {self.recipient.username}")
        super().delete(*args, **kwargs)
