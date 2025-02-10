from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Notification


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user information for notifications"""

    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications with related user information"""
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
        read_only_fields = [
            'id',
            'recipient',
            'actor',
            'notification_type',
            'message',
            'data',
            'created_at'
        ]
