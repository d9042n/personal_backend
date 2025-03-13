from typing import Dict, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
import logging

from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal user information serializer for notifications.
    
    This serializer provides only essential user information needed for
    notification display, reducing payload size and protecting user privacy.
    
    Fields:
        id: User's ID
        username: User's username
    """

    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = fields

    def to_representation(self, instance: User) -> Dict[str, Any]:
        """
        Convert user instance to dictionary representation.
        
        Args:
            instance: User instance to serialize
            
        Returns:
            Dict containing serialized user data
        """
        try:
            logger.debug(f"Serializing minimal user data for user {instance.username}")
            data = super().to_representation(instance)
            return data
        except Exception as e:
            logger.error(f"Error serializing minimal user data for user {instance.id}: {str(e)}", exc_info=True)
            raise


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications with related user information.
    
    This serializer handles the notification model and includes minimal
    information about related users (recipient and actor) through nested
    serialization.
    
    Fields:
        id: Notification ID
        recipient: Minimal user info for recipient
        actor: Minimal user info for actor (optional)
        notification_type: Type of notification
        message: Notification message
        data: Additional JSON data
        is_read: Read status
        created_at: Creation timestamp
    """
    
    recipient = UserMinimalSerializer(read_only=True)
    actor = UserMinimalSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor',
            'notification_type',
            'message',
            'data',
            'is_read',
            'created_at'
        ]
        read_only_fields = fields

    def to_representation(self, instance: Notification) -> Dict[str, Any]:
        """
        Convert notification instance to dictionary representation.
        
        This method adds custom handling for the data field to ensure
        it's always a dictionary, even if stored as null in database.
        
        Args:
            instance: Notification instance to serialize
            
        Returns:
            Dict containing serialized notification data
        """
        try:
            logger.debug(
                f"Serializing notification {instance.id} "
                f"(Type: {instance.notification_type}, Recipient: {instance.recipient.username})"
            )
            
            data = super().to_representation(instance)
            # Ensure data is always a dictionary
            data['data'] = data.get('data') or {}
            
            logger.debug(f"Successfully serialized notification {instance.id}")
            return data
            
        except Exception as e:
            logger.error(
                f"Error serializing notification {instance.id} for user {instance.recipient.id}: {str(e)}",
                exc_info=True
            )
            raise
