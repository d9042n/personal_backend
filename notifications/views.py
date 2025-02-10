from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class BaseNotificationView(APIView):
    """
    Base class for notification views with common permission logic
    """

    def get_permissions(self):
        return [permissions.IsAuthenticated()] if settings.API_REQUIRE_AUTH else [permissions.AllowAny()]

    def check_user_auth(self, request):
        """
        Check if user is authenticated when API_REQUIRE_AUTH is False
        Returns True if user can proceed, False if should return empty response
        """
        if not settings.API_REQUIRE_AUTH and isinstance(request.user, AnonymousUser):
            return False
        return True


class NotificationListView(BaseNotificationView):
    """
    API endpoint for listing user notifications
    """

    @swagger_auto_schema(
        operation_summary="List notifications",
        operation_description="""
        Get all notifications for the current user.
        
        Returns a list of notifications ordered by creation date (newest first).
        Each notification includes:
        * Notification ID
        * Recipient information
        * Actor information (if any)
        * Type of notification
        * Message
        * Additional data
        * Read status
        * Creation timestamp
        
        Notes:
        * Soft-deleted notifications are not included
        * Authentication may be required based on API_REQUIRE_AUTH setting
        """,
        responses={
            200: openapi.Response(
                description="List of notifications",
                schema=NotificationSerializer(many=True),
                examples={
                    "application/json": [{
                        "id": 1,
                        "recipient": {"id": 1, "username": "testuser"},
                        "actor": {"id": 2, "username": "admin"},
                        "notification_type": "profile_update",
                        "message": "Your profile has been updated",
                        "data": {"updated_fields": ["title"]},
                        "is_read": False,
                        "created_at": "2025-02-10T15:30:00Z"
                    }]
                }
            ),
            401: "Authentication credentials were not provided"
        },
        tags=['Notifications']
    )
    def get(self, request):
        if not self.check_user_auth(request):
            return Response([])

        notifications = Notification.objects.filter(
            recipient=request.user,
            is_deleted=False
        ).order_by('-created_at')

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationMarkReadView(BaseNotificationView):
    """
    API endpoint for marking notifications as read
    """

    @swagger_auto_schema(
        operation_summary="Mark notification as read",
        operation_description="""
        Mark a specific notification as read.
        
        Path Parameters:
        * pk (integer): The ID of the notification to mark as read
        
        Notes:
        * Only the recipient can mark their notifications as read
        * Returns 404 if notification doesn't exist or is soft-deleted
        * Authentication may be required based on API_REQUIRE_AUTH setting
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID of the notification to mark as read",
                type=openapi.TYPE_INTEGER,
                required=True,
                example=1
            )
        ],
        responses={
            200: openapi.Response(
                description="Notification marked as read",
                examples={
                    "application/json": {
                        "status": "marked as read"
                    }
                }
            ),
            401: "Authentication credentials were not provided",
            404: "Notification not found"
        },
        tags=['Notifications']
    )
    def post(self, request, pk):
        if not self.check_user_auth(request):
            return Response({"status": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        notification = get_object_or_404(
            Notification,
            id=pk,
            recipient=request.user,
            is_deleted=False
        )
        notification.mark_as_read()
        return Response({"status": "marked as read"})


class NotificationMarkAllReadView(BaseNotificationView):
    """
    API endpoint for marking all notifications as read
    """

    @swagger_auto_schema(
        operation_summary="Mark all notifications as read",
        operation_description="""
        Mark all unread notifications as read for the current user.
        
        This endpoint will:
        * Update all unread notifications to read status
        * Only affect notifications owned by the current user
        * Skip already read notifications
        * Skip soft-deleted notifications
        
        Notes:
        * This action cannot be undone
        * Authentication may be required based on API_REQUIRE_AUTH setting
        """,
        responses={
            200: openapi.Response(
                description="All notifications marked as read",
                examples={
                    "application/json": {
                        "status": "all marked as read"
                    }
                }
            ),
            401: "Authentication credentials were not provided"
        },
        tags=['Notifications']
    )
    def post(self, request):
        if not self.check_user_auth(request):
            return Response({"status": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        Notification.objects.filter(
            recipient=request.user,
            is_read=False,
            is_deleted=False
        ).update(is_read=True)
        return Response({"status": "all marked as read"})


class NotificationDeleteView(BaseNotificationView):
    """
    API endpoint for deleting a notification
    """

    @swagger_auto_schema(
        operation_summary="Delete notification",
        operation_description="""
        Soft delete a specific notification.
        
        Path Parameters:
        * pk (integer): The ID of the notification to delete
        
        This endpoint will:
        * Mark the notification as deleted (soft delete)
        * Remove it from future notification lists
        * Maintain the record in the database
        
        Notes:
        * Only the recipient can delete their notifications
        * Returns 404 if notification doesn't exist or is already deleted
        * Authentication may be required based on API_REQUIRE_AUTH setting
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID of the notification to delete",
                type=openapi.TYPE_INTEGER,
                required=True,
                example=1
            )
        ],
        responses={
            200: openapi.Response(
                description="Notification deleted",
                examples={
                    "application/json": {
                        "status": "deleted"
                    }
                }
            ),
            401: "Authentication credentials were not provided",
            404: "Notification not found"
        },
        tags=['Notifications']
    )
    def delete(self, request, pk):
        if not self.check_user_auth(request):
            return Response({"status": "not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        notification = get_object_or_404(
            Notification,
            id=pk,
            recipient=request.user,
            is_deleted=False
        )
        notification.soft_delete()
        return Response({"status": "deleted"})
