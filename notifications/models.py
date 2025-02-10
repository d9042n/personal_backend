from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import NotificationTypes


class Notification(models.Model):
    """
    Model to handle system notifications for users
    """
    # Core fields
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Recipient'),
        help_text=_('User who will receive the notification')
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_notifications',
        verbose_name=_('Actor'),
        help_text=_('User who triggered the notification (optional)')
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

    def mark_as_read(self):
        """Mark the notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read', 'updated_at'])

    def mark_as_unread(self):
        """Mark the notification as unread"""
        if self.is_read:
            self.is_read = False
            self.save(update_fields=['is_read', 'updated_at'])

    def soft_delete(self):
        """Soft delete the notification"""
        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=['is_deleted', 'updated_at'])
