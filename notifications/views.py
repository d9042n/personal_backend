from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)


class NotificationViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for managing notifications.
    
    This ViewSet provides endpoints for managing user notifications, including:
    - Listing all notifications for the authenticated user
    - Retrieving details of a specific notification
    - Marking notifications as read (single or all)
    - Soft deleting notifications
    
    All endpoints require authentication if API_REQUIRE_AUTH setting is True.
    Notifications are scoped to the authenticated user.
    """
    
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        """
        Get the permissions for the ViewSet.
        
        Returns:
            list: List of permission classes based on API_REQUIRE_AUTH setting
        """
        return [permissions.IsAuthenticated()] if settings.API_REQUIRE_AUTH else [permissions.AllowAny()]
    
    def get_queryset(self):
        """
        Get the queryset of notifications for the current user.
        
        Returns:
            QuerySet: Filtered queryset of non-deleted notifications for the user
        """
        if isinstance(self.request.user, AnonymousUser):
            return Notification.objects.none()
        return Notification.objects.filter(
            recipient=self.request.user,
            is_deleted=False
        ).order_by('-created_at')

    def perform_destroy(self, instance):
        """
        Perform soft delete instead of hard delete.
        
        Args:
            instance: The notification instance to delete
        """
        try:
            instance.soft_delete()
        except Exception as e:
            logger.error(f"Error soft deleting notification {instance.id}: {e}", exc_info=True)
            raise

    @swagger_auto_schema(
        operation_summary="List notifications",
        operation_description="Get all notifications for the authenticated user",
        responses={
            200: NotificationSerializer(many=True),
            401: "Authentication required"
        },
        tags=['Notifications']
    )
    def list(self, request):
        """
        List all notifications for the authenticated user.
        
        Returns:
            Response: List of serialized notifications
        """
        try:
            return super().list(request)
        except Exception as e:
            logger.error(f"Error listing notifications: {e}", exc_info=True)
            return Response(
                {"error": "Failed to retrieve notifications"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_summary="Get notification details",
        operation_description="Retrieve a specific notification",
        responses={
            200: NotificationSerializer,
            401: "Authentication required",
            404: "Notification not found"
        },
        tags=['Notifications']
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve details of a specific notification.
        
        Args:
            request: The HTTP request
            pk: Primary key of the notification
            
        Returns:
            Response: Serialized notification data
        """
        try:
            return super().retrieve(request)
        except Exception as e:
            logger.error(f"Error retrieving notification {pk}: {e}", exc_info=True)
            return Response(
                {"error": "Failed to retrieve notification"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_summary="Delete notification",
        operation_description="Soft delete a notification",
        responses={
            204: "Notification deleted",
            401: "Authentication required",
            404: "Notification not found"
        },
        tags=['Notifications']
    )
    def destroy(self, request, pk=None):
        """
        Soft delete a notification.
        
        Args:
            request: The HTTP request
            pk: Primary key of the notification
            
        Returns:
            Response: Empty response with appropriate status code
        """
        try:
            return super().destroy(request)
        except Exception as e:
            logger.error(f"Error deleting notification {pk}: {e}", exc_info=True)
            return Response(
                {"error": "Failed to delete notification"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_summary="Mark notification as read",
        responses={
            200: NotificationSerializer,
            401: "Authentication required",
            404: "Notification not found"
        },
        tags=['Notifications']
    )
    @action(detail=True, methods=['patch'])
    def read(self, request, pk=None):
        """
        Mark a single notification as read.
        
        Args:
            request: The HTTP request
            pk: Primary key of the notification
            
        Returns:
            Response: Updated notification data
        """
        try:
            notification = self.get_object()
            notification.mark_as_read()
            serializer = self.get_serializer(notification)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error marking notification {pk} as read: {e}", exc_info=True)
            return Response(
                {"error": "Failed to mark notification as read"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_summary="Mark all notifications as read",
        responses={
            200: NotificationSerializer(many=True),
            401: "Authentication required"
        },
        tags=['Notifications']
    )
    @action(detail=False, methods=['patch'])
    def read_all(self, request):
        """
        Mark all unread notifications as read.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: List of updated notifications
        """
        try:
            queryset = self.get_queryset().filter(is_read=False)
            queryset.update(is_read=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}", exc_info=True)
            return Response(
                {"error": "Failed to mark notifications as read"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
