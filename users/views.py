from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .serializers import UserSerializer, PublicUserSerializer, ProfileSerializer


# Create your views here.

class BaseAuthenticatedView:
    """Base class for handling API authentication"""
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if not settings.API_REQUIRE_AUTH:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class UserListCreateView(APIView):
    """
    API endpoints for listing and creating users
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        # Use settings variable instead of directly accessing env
        return [permissions.IsAuthenticated()] if settings.API_REQUIRE_AUTH else [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="""
        Retrieves a list of all users in the system.
        
        * Requires authentication
        * Staff users can see all users
        * Regular users can only see basic information
        """,
        responses={
            200: openapi.Response(
                description="Successfully retrieved the list of users",
                schema=UserSerializer(many=True),
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "example_user",
                        "email": "user@example.com",
                        "users": {
                            "profile": {
                                "name": "John Doe",
                                "title": "Software Engineer"
                            }
                        }
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided or are invalid"
            )
        },
        tags=['Users']
    )
    def get(self, request):
        # If authentication is not required and user is anonymous, return limited data
        if not settings.API_REQUIRE_AUTH and isinstance(request.user, AnonymousUser):
            users = User.objects.filter(is_active=True)  # Only show active users
            serializer = UserSerializer(users, many=True, context={'limited_fields': True})
            return Response(serializer.data)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create new user",
        operation_description="""
        Creates a new user account with profile information.
        
        Required fields:
        * username: Unique identifier for the user
        * email: Valid email address
        * password: Secure password meeting requirements
        
        Optional fields:
        * first_name: User's first name
        * last_name: User's last name
        * profile information: Professional and social details
        
        Notes:
        * Password must meet minimum security requirements
        * Email must be unique
        * Username must be unique
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Unique username",
                    example="user123"
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="email",
                    example="user@example.com"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="password",
                    example="SecurePass123!"
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="John"
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Doe"
                ),
                'users': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'profile': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'badge': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Available for hire"
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="John Doe"
                                ),
                                'title': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Software Developer"
                                ),
                                'description': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    example="Experienced software developer with expertise in web technologies."
                                ),
                                'github': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format="uri",
                                    example="https://github.com/username"
                                ),
                                'linkedin': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format="uri",
                                    example="https://linkedin.com/in/username"
                                ),
                                'twitter': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format="uri",
                                    example="https://twitter.com/username"
                                ),
                            }
                        )
                    }
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "user123",
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "users": {
                            "profile": {
                                "badge": "Available for hire",
                                "name": "John Doe",
                                "title": "Software Developer"
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "username": ["This username is already taken"],
                        "email": ["Enter a valid email address"],
                        "password": ["Password must be at least 8 characters long"]
                    }
                }
            )
        },
        tags=['Users']
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    API endpoints for retrieving, updating, and deleting specific users
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(
        operation_summary="Get user details",
        operation_description="""
        Retrieves detailed information about a specific user.
        
        Access Control:
        * Users can view their own details
        * Staff users can view any user's details
        * Regular users cannot view other users' details
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="The ID of the user to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True,
                example=1
            )
        ],
        responses={
            200: openapi.Response(
                description="User details retrieved successfully",
                schema=UserSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "example_user",
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "users": {
                            "profile": {
                                "badge": "Gold",
                                "name": "John Doe",
                                "title": "Senior Developer"
                            }
                        }
                    }
                }
            ),
            401: "Authentication credentials were not provided",
            403: "You do not have permission to view this user's details",
            404: "User not found"
        },
        tags=['Users']
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        if user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user",
        operation_description="""
        Updates information for a specific user.
        
        Access Control:
        * Users can update their own information
        * Staff users can update any user's information
        * Regular users cannot update other users' information
        
        Notes:
        * Partial updates are supported
        * Password updates require the current password
        * Email updates must be unique
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="The ID of the user to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="User updated successfully",
                schema=UserSerializer
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "email": ["This email is already in use"],
                        "profile": {
                            "github": ["Enter a valid URL"]
                        }
                    }
                }
            ),
            401: "Authentication credentials were not provided",
            403: "You do not have permission to update this user",
            404: "User not found"
        },
        tags=['Users']
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete user",
        operation_description="""
        Deletes a specific user account.
        
        Access Control:
        * Users can delete their own account
        * Staff users can delete any user account
        * Regular users cannot delete other users' accounts
        
        Notes:
        * This action is irreversible
        * All associated data will be deleted
        """,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="The ID of the user to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "User successfully deleted",
            401: "Authentication credentials were not provided",
            403: "You do not have permission to delete this user",
            404: "User not found"
        },
        tags=['Users']
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        if user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicUserView(APIView):
    """Public endpoint for viewing user profiles"""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @swagger_auto_schema(
        operation_summary="Get public profile",
        operation_description="Retrieve public profile information for any user",
        responses={
            200: PublicUserSerializer,
            404: "User not found"
        },
        tags=['Public']
    )
    def get(self, request, username):
        user = get_object_or_404(User, username=username, is_active=True)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class ProfileView(APIView):
    """
    API endpoint for managing authenticated user's profile
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get own profile",
        operation_description="Retrieve full profile information for authenticated user",
        responses={
            200: UserSerializer,
            401: "Authentication required"
        },
        tags=['Profile']
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update own profile",
        operation_description="""
        Update profile information for authenticated user.
        
        Supports partial updates for:
        * Basic information (name, email)
        * Profile details (title, bio)
        * Social links
        """,
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid data",
            401: "Authentication required"
        },
        tags=['Profile']
    )
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    """
    API endpoint for user registration
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Register new user",
        operation_description="""
        Create a new user account.
        
        Required fields:
        * username
        * email
        * password
        
        Optional fields:
        * profile information
        """,
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Invalid data"
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, BaseAuthenticatedView):
    """ViewSet for managing user accounts and profiles"""
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        # Check permissions for modification operations
        if self.action in ['update', 'partial_update', 'destroy', 'update_profile']:
            if user != self.request.user and not self.request.user.is_staff:
                raise PermissionDenied("You don't have permission to modify this user")
        return user

    @swagger_auto_schema(
        operation_summary="Create user account",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Invalid data"
        },
        tags=['Users']
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get user details",
        responses={
            200: UserSerializer,
            404: "User not found"
        },
        tags=['Users']
    )
    def retrieve(self, request, username):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid data",
            403: "Permission denied",
            404: "User not found"
        },
        tags=['Users']
    )
    def update(self, request, username):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update user",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid data",
            403: "Permission denied",
            404: "User not found"
        },
        tags=['Users']
    )
    def partial_update(self, request, username):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get user profile",
        responses={
            200: openapi.Response(
                description="User profile retrieved successfully",
                examples={
                    "application/json": {
                        "username": "johndoe",
                        "profile": {
                            "is_available": True,
                            "badge": "Available",
                            "name": "John Doe",
                            "title": "Senior Developer",
                            "description": "Full-stack developer",
                            "social_links": {
                                "github": "https://github.com/johndoe",
                                "linkedin": "https://linkedin.com/in/johndoe",
                                "twitter": "https://twitter.com/johndoe",
                                "facebook": "https://facebook.com/johndoe",
                                "leetcode": "https://leetcode.com/johndoe",
                                "hackerrank": "https://hackerrank.com/johndoe",
                                "medium": "https://medium.com/@johndoe",
                                "stackoverflow": "https://stackoverflow.com/users/123/johndoe",
                                "portfolio": "https://johndoe.dev",
                                "youtube": "https://youtube.com/@johndoe",
                                "devto": "https://dev.to/johndoe"
                            }
                        }
                    }
                }
            ),
            404: "User not found"
        },
        tags=['Profiles']
    )
    def profile(self, request, username):
        user = self.get_object()
        profile = user.users.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update profile",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'badge': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'github': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'linkedin': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'twitter': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'facebook': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'leetcode': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'hackerrank': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'medium': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'stackoverflow': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'portfolio': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'youtube': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
                'devto': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            }
        ),
        responses={
            200: ProfileSerializer,
            400: "Invalid data",
            403: "Permission denied",
            404: "User not found"
        },
        tags=['Profiles']
    )
    def update_profile(self, request, username):
        user = self.get_object()
        profile = user.users.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete user",
        responses={
            204: "User deleted",
            403: "Permission denied",
            404: "User not found"
        },
        tags=['Users']
    )
    def destroy(self, request, username):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
