from typing import List, Tuple, Dict

from django.utils.translation import gettext_lazy as _


class NotificationTypes:
    """
    Constants for notification types.
    
    This class defines the available notification types in the system and provides
    methods for validation. Each notification type has a corresponding human-readable
    label that can be used in the UI.
    
    Available notification types:
        PROFILE_UPDATE: Used when a user's profile is updated
        MENTION: Used when a user is mentioned in content
        SYSTEM: Used for system-level notifications
        SESSION_TERMINATED: Used when a user's session is terminated
        SESSIONS_TERMINATED: Used when multiple sessions are terminated
    """
    
    class Types:
        """Available notification types in the system."""
        PROFILE_UPDATE = 'profile_update'
        MENTION = 'mention'
        SYSTEM = 'system'
        SESSION_TERMINATED = 'session_terminated'
        SESSIONS_TERMINATED = 'sessions_terminated'
        
        # Choices for model field
        CHOICES: List[Tuple[str, str]] = [
            (PROFILE_UPDATE, _('Profile Update')),
            (MENTION, _('Mention')),
            (SYSTEM, _('System Notification')),
            (SESSION_TERMINATED, _('Session Terminated')),
            (SESSIONS_TERMINATED, _('Multiple Sessions Terminated')),
        ]
    
    # For direct access
    PROFILE_UPDATE = Types.PROFILE_UPDATE
    MENTION = Types.MENTION
    SYSTEM = Types.SYSTEM
    SESSION_TERMINATED = Types.SESSION_TERMINATED
    SESSIONS_TERMINATED = Types.SESSIONS_TERMINATED
    
    # Choices for model field
    CHOICES = Types.CHOICES
    
    # Cache for valid types
    _VALID_TYPES: Dict[str, str] = dict(CHOICES)

    @classmethod
    def is_valid_type(cls, notification_type: str) -> bool:
        """
        Check if a notification type is valid.
        
        Args:
            notification_type: The notification type to validate
            
        Returns:
            bool: True if the notification type is valid, False otherwise
        """
        return notification_type in cls._VALID_TYPES
