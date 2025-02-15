from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import Notification
from .serializers import NotificationSerializer


class AuthMixin:
    """Mixin to handle authentication logic"""
    
    def get_permissions(self):
        return [permissions.IsAuthenticated()] if settings.API_REQUIRE_AUTH else [permissions.AllowAny()]
    
    def check_user_auth(self, request):
        """Check if user can access notifications"""
        if not settings.API_REQUIRE_AUTH and isinstance(request.user, AnonymousUser):
            return False
        return True


class NotificationViewSet(AuthMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for managing notifications.
    
    Endpoints:
    - GET /notifications/ - List all notifications
    - GET /notifications/{id}/ - Get single notification
    - DELETE /notifications/{id}/ - Delete notification
    - PATCH /notifications/{id}/read/ - Mark as read
    """
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        if not self.check_user_auth(self.request):
            return Notification.objects.none()
        return Notification.objects.filter(
            recipient=self.request.user,
            is_deleted=False
        ).order_by('-created_at')

    def perform_destroy(self, instance):
        instance.soft_delete()

    @swagger_auto_schema(
        operation_summary="Mark notification as read",
        responses={
            200: NotificationSerializer,
            401: "Unauthorized",
            404: "Not found"
        }
    )
    @action(detail=True, methods=['patch'])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)


class NotificationBulkUpdateView(AuthMixin, APIView):
    """Bulk operations on notifications"""
    
    @swagger_auto_schema(
        operation_summary="Mark all notifications as read",
        responses={
            200: NotificationSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def patch(self, request):
        if not self.check_user_auth(request):
            return Response(
                {"detail": "Authentication required"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False,
            is_deleted=False
        )
        notifications.update(is_read=True)
        
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationDeleteView(AuthMixin, APIView):
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
