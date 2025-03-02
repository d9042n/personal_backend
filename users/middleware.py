import logging
import threading
from typing import Optional

import requests
from django.http import HttpResponse
from django.utils import timezone
from user_agents import parse

from .models import UserSession

logger = logging.getLogger(__name__)


class UserSessionMiddleware:
    """
    Middleware for handling user sessions and tracking user activity.
    
    This middleware performs the following tasks:
    1. Tracks user sessions and their activity
    2. Parses user agent information
    3. Determines device type
    4. Tracks IP address and geolocation
    5. Manages session expiration
    6. Cleans up expired sessions
    
    The middleware uses asynchronous processing for geolocation lookups to
    avoid impacting response times.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process each request through the middleware.
        
        Args:
            request: The incoming HTTP request
            
        Returns:
            HttpResponse: The response from the next middleware or view
        """
        if request.user.is_authenticated:
            try:
                response = self._handle_authenticated_user(request)
                if response:  # Early return for expired sessions
                    return response
            except Exception as e:
                logger.error(f"Critical error in UserSessionMiddleware: {str(e)}", exc_info=True)
                # Continue processing even if session handling fails

        return self.get_response(request)

    def _handle_authenticated_user(self, request) -> Optional[HttpResponse]:
        """
        Handle session management for authenticated users.
        
        Args:
            request: The incoming HTTP request
            
        Returns:
            Optional[HttpResponse]: Response for expired sessions, None otherwise
        """
        session_key = request.session.session_key
        
        # Parse user agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        device_type = self._determine_device_type(user_agent)
        
        # Get IP
        ip_address = self.get_client_ip(request)

        # Update or create session
        user_session = self._update_or_create_session(
            request.user,
            session_key,
            user_agent_string,
            device_type,
            ip_address
        )

        if not user_session:
            return None

        # Handle expired session
        if user_session.is_expired():
            user_session.terminate()
            return HttpResponse('Session expired.', status=401)

        # Cleanup other expired sessions
        self._cleanup_expired_sessions(request.user)
        
        return None

    def _determine_device_type(self, user_agent) -> str:
        """
        Determine the type of device from user agent.
        
        Args:
            user_agent: Parsed user agent object
            
        Returns:
            str: Device type ('mobile', 'tablet', or 'pc')
        """
        if user_agent.is_mobile:
            return 'mobile'
        elif user_agent.is_tablet:
            return 'tablet'
        return 'pc'

    def _update_or_create_session(self, user, session_key, user_agent_string, device_type, ip_address):
        """
        Update existing session or create a new one.
        
        Args:
            user: The authenticated user
            session_key: The session key
            user_agent_string: Raw user agent string
            device_type: Determined device type
            ip_address: Client IP address
            
        Returns:
            UserSession: The updated or created session object
        """
        try:
            user_session, created = UserSession.objects.update_or_create(
                user=user,
                session_key=session_key,
                defaults={
                    'last_activity': timezone.now(),
                    'expires_at': timezone.now() + timezone.timedelta(minutes=30),
                    'ip_address': ip_address,
                    'user_agent': user_agent_string,
                    'device_type': device_type,
                    'is_active': True
                }
            )

            # Start location lookup in background only for new sessions or missing locations
            if created or not user_session.location:
                self.update_location_async(user_session.id, ip_address)

            return user_session

        except Exception as e:
            logger.error(f"Error updating/creating session: {str(e)}", exc_info=True)
            return None

    def _cleanup_expired_sessions(self, user):
        """
        Clean up expired sessions for a user.
        
        Args:
            user: The user whose expired sessions to clean up
        """
        try:
            UserSession.objects.filter(
                user=user,
                expires_at__lt=timezone.now(),
                is_active=True
            ).update(is_active=False)
        except Exception as e:
            logger.error(f"Error cleaning up expired sessions: {str(e)}", exc_info=True)

    def get_client_ip(self, request) -> str:
        """
        Get client IP address from request.
        
        Args:
            request: The HTTP request
            
        Returns:
            str: The client's IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')

    def update_location_async(self, session_id: int, ip_address: str):
        """
        Update session location asynchronously.
        
        Args:
            session_id: ID of the session to update
            ip_address: IP address to look up location for
        """
        def _update_location():
            try:
                location = self.get_location(ip_address)
                if location:
                    UserSession.objects.filter(id=session_id).update(location=location)
            except Exception as e:
                logger.error(f"Error updating location for session {session_id}: {str(e)}", exc_info=True)

        thread = threading.Thread(target=_update_location)
        thread.daemon = True
        thread.start()

    def get_location(self, ip_address: str) -> Optional[str]:
        """
        Get location information for an IP address.
        
        Args:
            ip_address: IP address to look up
            
        Returns:
            Optional[str]: Location string in "City, Country" format, or None if lookup fails
        """
        if not ip_address or ip_address in ('127.0.0.1', 'localhost'):
            return None

        try:
            response = requests.get(
                f'https://ipapi.co/{ip_address}/json/',
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            # Check for error response
            if data.get('error'):
                logger.warning(f"IP lookup error for {ip_address}: {data['error']}")
                return None
                
            city = data.get('city', '').strip()
            country = data.get('country_name', '').strip()
            
            if city and country:
                return f"{city}, {country}"
            elif country:
                return country
            return None
            
        except requests.RequestException as e:
            logger.warning(f"Failed to get location for IP {ip_address}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting location for IP {ip_address}: {str(e)}", exc_info=True)
            return None 