from django.urls import path
from .views import (
    NotificationViewSet,
    NotificationBulkUpdateView
)
from rest_framework.routers import DefaultRouter

app_name = 'notifications'

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('bulk/read/', NotificationBulkUpdateView.as_view(), name='notification-bulk-update'),
] + router.urls
