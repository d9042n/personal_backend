from django.urls import path

from .views import UserViewSet, PublicUserView

urlpatterns = [
    # Public endpoints
    path('public/profile/<str:username>/', PublicUserView.as_view(), name='public-profile'),

    # User management endpoints
    path('users/', UserViewSet.as_view({
        'post': 'create'
    }), name='user-register'),
    path('users/<str:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-detail'),
]
