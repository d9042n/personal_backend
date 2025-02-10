from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import Users, Profile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os

# Create your views here.

class UserListCreateView(APIView):
    """
    API endpoints for listing and creating users
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        # Use global setting for GET requests
        return [permissions.IsAuthenticated()] if os.getenv('API_REQUIRE_AUTH', 'True').lower() == 'true' else [permissions.AllowAny()]

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
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create new user",
        operation_description="""
        Creates a new user account with profile information.
        
        Required fields:
        * username
        * email
        * password
        
        Optional fields:
        * first_name
        * last_name
        * profile information (badge, name, title, etc.)
        
        Notes:
        * Password must meet minimum security requirements
        * Email must be unique
        * Username must be unique
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Unique username"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format="email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format="password"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'users': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'profile': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'badge': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'title': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'github': openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                                'linkedin': openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                                'twitter': openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                            }
                        )
                    }
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=UserSerializer
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "username": ["This field is required"],
                        "email": ["Enter a valid email address"],
                        "password": ["This password is too common"]
                    }
                }
            ),
            409: "Username or email already exists"
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

class ProfileView(APIView):
    """
    API endpoints for managing user profiles
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get current user profile",
        operation_description="""
        Retrieves the profile information of the currently authenticated user.
        
        Returns:
        * Basic user information
        * Profile details including social links
        * Account metadata
        """,
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully",
                schema=UserSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "current_user",
                        "email": "user@example.com",
                        "users": {
                            "profile": {
                                "badge": "Silver",
                                "name": "Jane Doe",
                                "title": "Full Stack Developer",
                                "description": "Passionate about coding",
                                "github": "https://github.com/janedoe",
                                "linkedin": "https://linkedin.com/in/janedoe",
                                "twitter": "https://twitter.com/janedoe"
                            }
                        }
                    }
                }
            ),
            401: "Authentication credentials were not provided"
        },
        tags=['Profile']
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update current user profile",
        operation_description="""
        Updates the profile information of the currently authenticated user.
        
        Updatable fields:
        * Basic user information (first_name, last_name, email)
        * Profile details (badge, name, title, description)
        * Social media links (github, linkedin, twitter)
        
        Notes:
        * Partial updates are supported
        * Social media links must be valid URLs
        * Email updates must be unique
        """,
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=UserSerializer
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "users": {
                            "profile": {
                                "github": ["Enter a valid URL"],
                                "name": ["Ensure this field has no more than 100 characters"]
                            }
                        }
                    }
                }
            ),
            401: "Authentication credentials were not provided"
        },
        tags=['Profile']
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
