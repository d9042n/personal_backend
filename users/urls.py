from django.urls import path

from .views import UserListCreateView, UserDetailView, ProfileView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
