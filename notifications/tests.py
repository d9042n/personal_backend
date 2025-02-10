from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Notification


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type='test',
            message='Test notification'
        )
        self.assertEqual(str(notification), f"Notification for testuser: Test notification")
        self.assertFalse(notification.is_read)
        self.assertFalse(notification.is_deleted)


class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type='test',
            message='Test notification'
        )

    def test_list_notifications(self):
        url = reverse('notifications:notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_notification_read(self):
        url = reverse('notifications:notification-mark-read', args=[self.notification.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
