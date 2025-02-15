from django.urls import path

from .views import UserViewSet, PublicUserView

urlpatterns = [
    # Public endpoints
    path('users/public/<str:username>/', PublicUserView.as_view(), name='public-profile'),

    # Protected endpoints
    path('users/', UserViewSet.as_view({
        'post': 'create'
    }), name='user-create'),
    
    path('users/<str:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='user-detail'),
    
    path('users/<str:username>/profile/', UserViewSet.as_view({
        'get': 'profile',
        'patch': 'update_profile'
    }), name='user-profile'),
]
