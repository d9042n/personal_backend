from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserSession
from .serializers import UserSerializer, PublicUserSerializer, ProfileSerializer, UserSessionSerializer
from notifications.services import NotificationService
from notifications.constants import NotificationTypes

# Base class for handling API authentication
class BaseAuthenticatedView:
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if not settings.API_REQUIRE_AUTH:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


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
        operation_summary="Create new user",
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
                'social_links': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
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
                        'devto': openapi.Schema(type=openapi.TYPE_STRING, format='uri')
                    }
                )
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
        operation_summary="Partially update user",
        operation_description="""
        Partially update user information. Only provided fields will be updated.
        
        Supports updating:
        * Basic user information (username, email, first/last name)
        * Profile information (title, bio, availability)
        * Social media links
        * Password
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'profile': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'is_available': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'badge': openapi.Schema(type=openapi.TYPE_STRING),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'social_links': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
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
                                'devto': openapi.Schema(type=openapi.TYPE_STRING, format='uri')
                            }
                        )
                    }
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="User updated successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
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
            400: openapi.Response(description="Invalid data provided"),
            401: openapi.Response(description="Authentication required"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="User not found")
        },
        tags=['Users']
    )
    def partial_update(self, request, username):
        """
        Partially update user information.
        Only provided fields will be updated while others remain unchanged.
        """
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]

    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description="Authenticate a user using username or email and return JWT tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username_or_email', 'password'],
            properties={
                'username_or_email': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Username or email address'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='User password'
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "refresh": "refresh_token",
                        "access": "access_token",
                        "user": {
                            "id": 1,
                            "username": "example_user",
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    }
                }
            ),
            401: openapi.Response(description="Invalid credentials.")
        },
        tags=['Authentication']
    )
    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        # Try to authenticate with username
        user = authenticate(username=username_or_email, password=password)
        
        # If authentication with username fails, try with email
        if user is None:
            try:
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # Ensure session exists and get session key
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # Get request metadata
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)
        device_type = self.get_device_type(user_agent_string)

        # Update or create session
        UserSession.objects.update_or_create(
            user=user,
            session_key=session_key,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent_string,
                'device_type': device_type,
                'expires_at': timezone.now() + timezone.timedelta(days=7),
                'is_active': True
            }
        )

        # Return response with tokens and user data
        return Response({
            'refresh': str(refresh),
            'access': access,
            'user': UserSerializer(user, context={'limited_fields': True}).data
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def get_device_type(self, user_agent_string):
        from user_agents import parse
        user_agent = parse(user_agent_string)
        if user_agent.is_mobile:
            return 'mobile'
        elif user_agent.is_tablet:
            return 'tablet'
        return 'pc'


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="Log out the user by blacklisting their JWT tokens and invalidating the current session.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The refresh token to blacklist'
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Successfully logged out",
                examples={
                    "application/json": {
                        "detail": "Successfully logged out."
                    }
                }
            ),
            400: openapi.Response(description="Invalid token."),
            401: openapi.Response(description="Authentication credentials were not provided.")
        },
        tags=['Authentication']
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Invalidate user session
            if request.session.session_key:
                UserSession.objects.filter(
                    user=request.user,
                    session_key=request.session.session_key,
                    is_active=True
                ).update(is_active=False)

            return Response({'detail': 'Successfully logged out.'})

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get User Sessions",
        operation_description="Retrieve all active sessions for the authenticated user.",
        responses={
            200: UserSessionSerializer(many=True),
            204: openapi.Response(description="No active sessions found.")
        },
        tags=['Sessions']
    )
    def get(self, request):
        """Retrieve all active sessions for the authenticated user."""
        user_sessions = request.user.sessions.filter(is_active=True)
        if not user_sessions:
            return Response({"detail": "No active sessions found."}, status=status.HTTP_204_NO_CONTENT)

        # Renew sessions upon activity
        for session in user_sessions:
            session.last_activity = timezone.now()
            session.save()

        serializer = UserSessionSerializer(user_sessions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Invalidate User Session",
        operation_description="Invalidate specific session or all sessions except current",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'session_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Specific session ID to invalidate (optional)'
                ),
                'all_except_current': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='Invalidate all sessions except current'
                ),
            }
        ),
        responses={
            204: openapi.Response(description="Session(s) invalidated."),
            400: openapi.Response(description="Invalid request parameters."),
            404: openapi.Response(description="Session not found.")
        },
        tags=['Sessions']
    )
    def delete(self, request):
        """Invalidate user session(s)."""
        session_id = request.data.get('session_id')
        all_except_current = request.data.get('all_except_current', False)

        if session_id:
            try:
                session = UserSession.objects.get(
                    id=session_id,
                    user=request.user,
                    is_active=True
                )
                session.terminate()
                return Response({"detail": "Session invalidated."}, status=status.HTTP_204_NO_CONTENT)
            except UserSession.DoesNotExist:
                return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        if all_except_current:
            current_session_key = request.session.session_key
            other_sessions = UserSession.objects.filter(
                user=request.user,
                is_active=True
            ).exclude(session_key=current_session_key)

            for session in other_sessions:
                session.terminate()

            NotificationService.create_notification(
                recipient=request.user,
                notification_type=NotificationTypes.SESSIONS_TERMINATED,
                message="All other sessions have been terminated",
                extra_data={
                    'terminated_count': other_sessions.count(),
                    'current_session_key': current_session_key
                }
            )

            return Response({"detail": "All other sessions invalidated."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Invalid request parameters."}, status=status.HTTP_400_BAD_REQUEST)
