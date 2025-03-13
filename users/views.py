from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import logging

from notifications.constants import NotificationTypes
from notifications.services import NotificationService
from .models import UserSession
from .serializers import (
    ProfileSerializer,
    PublicUserSerializer,
    UserSerializer,
    UserSessionSerializer
)

logger = logging.getLogger(__name__)

# Base class for handling API authentication
class BaseAuthenticatedView:
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if not settings.API_REQUIRE_AUTH:
            logger.debug("API authentication requirement is disabled")
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
        logger.info(f"Public profile request for user: {username}")
        try:
            user = get_object_or_404(User, username=username, is_active=True)
            serializer = PublicUserSerializer(user)
            logger.debug(f"Successfully retrieved public profile for user: {username}")
            return Response(serializer.data)
        except User.DoesNotExist:
            logger.warning(f"Public profile request failed - user not found: {username}")
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ViewSet, BaseAuthenticatedView):
    """ViewSet for managing user accounts and profiles"""
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            logger.debug("Allowing unauthenticated access to user creation")
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        # Check permissions for modification operations
        if self.action in ['update', 'partial_update', 'destroy', 'update_profile']:
            if user != self.request.user and not self.request.user.is_staff:
                logger.warning(f"Permission denied - User {self.request.user.username} attempted to modify {username}")
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
        logger.info("User creation request received")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"User created successfully: {user.username}")
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}", exc_info=True)
                return Response({"detail": "Error creating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.warning(f"Invalid user creation data: {serializer.errors}")
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
        logger.info(f"Profile retrieval request for user: {username}")
        try:
            user = self.get_object()
            serializer = UserSerializer(user)
            logger.debug(f"Successfully retrieved profile for user: {username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving user profile for {username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error retrieving profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        logger.info(f"Profile update request for user: {username}")
        try:
            user = self.get_object()
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"Successfully updated profile for user: {username}")
                return Response(UserSerializer(user).data)
            logger.warning(f"Invalid profile update data for {username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating profile for {username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error updating profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        logger.info(f"Account deletion request for user: {username}")
        try:
            user = self.get_object()
            user.delete()
            logger.info(f"Successfully deleted user account: {username}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user account {username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error deleting account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        logger.info(f"Login attempt for user: {username_or_email}")

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
            logger.warning(f"Failed login attempt for user: {username_or_email}")
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            logger.warning(f"Login attempt for disabled account: {username_or_email}")
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
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

            logger.info(f"Successful login for user {user.username} from {ip_address} ({device_type})")

            # Return response with tokens and user data
            return Response({
                'refresh': str(refresh),
                'access': access,
                'user': UserSerializer(user, context={'limited_fields': True}).data
            })
        except Exception as e:
            logger.error(f"Error during login process for {username_or_email}: {str(e)}", exc_info=True)
            return Response({"detail": "Error during login"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        logger.info(f"Logout request for user: {request.user.username}")
        try:
            # Get current session
            session_key = request.session.session_key
            if session_key:
                session = UserSession.objects.filter(
                    user=request.user,
                    session_key=session_key,
                    is_active=True
                ).first()
                
                if session:
                    session.terminate()
                    logger.info(f"Successfully terminated session for user: {request.user.username}")
                
            # Cleanup any expired sessions
            expired_count = UserSession.objects.cleanup_expired()
            if expired_count:
                logger.info(f"Cleaned up {expired_count} expired sessions during logout")

            return Response({"detail": "Successfully logged out"})
        except Exception as e:
            logger.error(f"Error during logout for user {request.user.username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error during logout"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        logger.info(f"Session list request for user: {request.user.username}")
        try:
            sessions = UserSession.objects.get_user_active_sessions(request.user)
            serializer = UserSessionSerializer(sessions, many=True)
            logger.debug(f"Retrieved {len(sessions)} active sessions for user: {request.user.username}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving sessions for user {request.user.username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error retrieving sessions"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        logger.info(f"Session invalidation request for user: {request.user.username}")
        
        session_id = request.data.get('session_id')
        all_except_current = request.data.get('all_except_current', False)

        try:
            if session_id:
                try:
                    session = UserSession.objects.get(
                        id=session_id,
                        user=request.user,
                        is_active=True
                    )
                    session.terminate()
                    logger.info(f"Successfully terminated session {session_id} for user: {request.user.username}")
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except UserSession.DoesNotExist:
                    logger.warning(f"Session {session_id} not found for user: {request.user.username}")
                    return Response({"detail": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

            if all_except_current:
                current_session_key = request.session.session_key
                other_sessions = UserSession.objects.filter(
                    user=request.user,
                    is_active=True
                ).exclude(session_key=current_session_key)

                terminated_count = 0
                for session in other_sessions:
                    session.terminate()
                    terminated_count += 1

                logger.info(f"Terminated {terminated_count} other sessions for user: {request.user.username}")

                NotificationService.create_notification(
                    recipient=request.user,
                    notification_type=NotificationTypes.SESSIONS_TERMINATED,
                    message=f"All other sessions have been terminated ({terminated_count} sessions)",
                    extra_data={
                        'terminated_count': terminated_count,
                        'current_session_key': current_session_key
                    }
                )

                return Response(status=status.HTTP_204_NO_CONTENT)

            logger.warning(f"Invalid session invalidation request parameters for user: {request.user.username}")
            return Response({"detail": "Invalid request parameters"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error during session invalidation for user {request.user.username}: {str(e)}", exc_info=True)
            return Response({"detail": "Error during session invalidation"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
