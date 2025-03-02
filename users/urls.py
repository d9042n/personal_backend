from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, PublicUserView, UserLoginView, UserLogoutView, UserSessionView

urlpatterns = [
    # Public endpoints
    path('users/public/<str:username>/', PublicUserView.as_view(), name='public-profile'),

    # Authentication endpoints
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
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

    path('session/', UserSessionView.as_view(), name='session'),
]
