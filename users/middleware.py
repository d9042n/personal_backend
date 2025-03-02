from django.utils import timezone
from django.http import HttpResponse
from user_agents import parse
from .models import UserSession
import requests
import threading
import logging

logger = logging.getLogger(__name__)


class UserSessionMiddleware:
    """Middleware for handling user sessions and tracking user activity."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            
            # Parse user agent
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            device_type = 'mobile' if user_agent.is_mobile else 'tablet' if user_agent.is_tablet else 'pc'
            
            # Get IP
            ip_address = self.get_client_ip(request)

            try:
                # Update or create session without waiting for location
                user_session, created = UserSession.objects.update_or_create(
                    user=request.user,
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

                # Check if session is expired
                if user_session.is_expired():
                    user_session.terminate()
                    return HttpResponse('Session expired.', status=401)

                # Cleanup other expired sessions for this user
                UserSession.objects.filter(
                    user=request.user,
                    expires_at__lt=timezone.now(),
                    is_active=True
                ).update(is_active=False)

            except Exception as e:
                logger.error(f"Error in UserSessionMiddleware: {str(e)}")
                # Continue processing even if session handling fails
                pass

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def update_location_async(self, session_id, ip_address):
        """Update session location asynchronously."""
        def _update_location():
            try:
                location = self.get_location(ip_address)
                if location:
                    UserSession.objects.filter(id=session_id).update(location=location)
            except Exception as e:
                logger.error(f"Error updating location for session {session_id}: {str(e)}")

        thread = threading.Thread(target=_update_location)
        thread.daemon = True
        thread.start()

    def get_location(self, ip_address):
        """Get location information for an IP address."""
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
            logger.error(f"Unexpected error getting location for IP {ip_address}: {str(e)}")
            return None 