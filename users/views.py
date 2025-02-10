from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializers import UserSerializer, PublicUserSerializer
from .services import UserService


# Create your views here.

class BaseAuthenticatedView:
    """Base class for handling API_REQUIRE_AUTH setting"""
    throttle_classes = [UserRateThrottle]  # Add rate limiting
    
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
    """Public API endpoint for retrieving user profiles"""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]  # Add rate limiting for public endpoint

    @swagger_auto_schema(
        operation_summary="Get public profile",
        operation_description="""
        Retrieve public profile information for any user by username.
        
        This endpoint:
        * Is always publicly accessible
        * Does not require authentication
        * Returns only non-sensitive information
        * Rate limited to 100 requests/day
        
        URL: /api/public/profile/{username}/
        """,
        responses={
            200: PublicUserSerializer,
            404: "User not found",
            429: "Too many requests - rate limit exceeded"
        },
        tags=['Public Access']
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
        
        # For update/delete operations, check user permissions
        if self.action in ['partial_update', 'destroy']:
            if user != self.request.user and not self.request.user.is_staff:
                raise PermissionDenied("You don't have permission to modify this user")
        return user

    @swagger_auto_schema(
        operation_summary="Register new account",
        operation_description="""
        Create a new user account with profile information.
        
        This endpoint:
        * Is always publicly accessible
        * Does not require authentication
        * Allows new users to register
        
        Required fields:
        * username (unique)
        * email (unique)
        * password
        
        Optional:
        * Profile information
        * Social media links
        """,
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Invalid data - see response for details"
        },
        tags=['Public Access']
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get user profile",
        operation_description="""
        Retrieve complete user profile information.
        
        Authentication:
        * Required if API_REQUIRE_AUTH is True
        * Optional if API_REQUIRE_AUTH is False
        
        Note: For public profile access, use /api/public/profile/{username}/ instead
        """,
        responses={
            200: UserSerializer,
            401: "Authentication required when API_REQUIRE_AUTH is True",
            404: "User not found"
        },
        tags=['Protected Access']
    )
    def retrieve(self, request, username):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="""
        Update user profile information.
        
        Authentication:
        * Required if API_REQUIRE_AUTH is True
        * Optional if API_REQUIRE_AUTH is False
        
        Authorization:
        * Users can only update their own profile
        * Staff users can update any profile
        
        Supports partial updates for:
        * Basic information (name, email)
        * Profile details (title, bio)
        * Social links
        """,
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Invalid data",
            401: "Authentication required when API_REQUIRE_AUTH is True",
            403: "Permission denied - can only modify own profile",
            404: "User not found"
        },
        tags=['Protected Access']
    )
    def partial_update(self, request, username):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete user account",
        operation_description="""
        Permanently delete user account and all associated data.
        
        Authentication:
        * Required if API_REQUIRE_AUTH is True
        * Optional if API_REQUIRE_AUTH is False
        
        Authorization:
        * Users can only delete their own account
        * Staff users can delete any account
        """,
        responses={
            204: "Account deleted successfully",
            401: "Authentication required when API_REQUIRE_AUTH is True",
            403: "Permission denied - can only delete own account",
            404: "User not found"
        },
        tags=['Protected Access']
    )
    def destroy(self, request, username):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
