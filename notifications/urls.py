"""
URL configuration for the notifications app.

This module defines the URL patterns for the notifications API endpoints.
All routes are registered using DRF's DefaultRouter for consistent
RESTful URL structure.

Available endpoints:
    GET /notifications/ - List all notifications
    GET /notifications/{id}/ - Retrieve a specific notification
    DELETE /notifications/{id}/ - Delete a notification
    PATCH /notifications/{id}/read/ - Mark a notification as read
    PATCH /notifications/read_all/ - Mark all notifications as read
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

app_name = 'notifications'

router = DefaultRouter()
router.register('', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
