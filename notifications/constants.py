from django.utils.translation import gettext_lazy as _


class NotificationTypes:
    """Constants for notification types"""
    PROFILE_UPDATE = 'profile_update'
    MENTION = 'mention'
    SYSTEM = 'system'

    CHOICES = [
        (PROFILE_UPDATE, _('Profile Update')),
        (MENTION, _('Mention')),
        (SYSTEM, _('System Notification')),
    ]

    @classmethod
    def is_valid_type(cls, notification_type):
        """Check if a notification type is valid"""
        return notification_type in dict(cls.CHOICES)
