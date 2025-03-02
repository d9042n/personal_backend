from typing import Dict, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Notification

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
        data = super().to_representation(instance)
        # Ensure data is always a dictionary
        data['data'] = data.get('data') or {}
        return data
