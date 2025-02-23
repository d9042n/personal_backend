from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet for managing notifications.
    
    Provides endpoints for:
    - Listing notifications
    - Retrieving single notifications
    - Marking notifications as read
    - Deleting notifications
    - Bulk operations on notifications
    """
    serializer_class = NotificationSerializer
    
    def get_permissions(self):
        return [permissions.IsAuthenticated()] if settings.API_REQUIRE_AUTH else [permissions.AllowAny()]
    
    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Notification.objects.none()
        return Notification.objects.filter(
            recipient=self.request.user,
            is_deleted=False
        ).order_by('-created_at')

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        instance.soft_delete()

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
        return super().list(request)

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
        return super().retrieve(request)

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
        return super().destroy(request)

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
        """Mark a single notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

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
        """Mark all unread notifications as read"""
        queryset = self.get_queryset().filter(is_read=False)
        queryset.update(is_read=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
