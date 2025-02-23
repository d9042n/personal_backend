from django.utils import timezone
from user_agents import parse
from .models import UserSession
import requests
from rest_framework.response import Response
from rest_framework import status

class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            
            # Parse user agent
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            device_type = 'mobile' if user_agent.is_mobile else 'tablet' if user_agent.is_tablet else 'pc'
            
            # Get IP and location
            ip_address = self.get_client_ip(request)
            location = self.get_location(ip_address)

            # Update or create session
            user_session, created = UserSession.objects.update_or_create(
                user=request.user,
                session_key=session_key,
                defaults={
                    'last_activity': timezone.now(),
                    'expires_at': timezone.now() + timezone.timedelta(minutes=30),  # Renew expiration
                    'ip_address': ip_address,
                    'user_agent': user_agent_string,
                    'device_type': device_type,
                    'location': location,
                    'is_active': True
                }
            )

            # Check if session is expired
            if user_session.is_expired():
                user_session.terminate()  # Terminate expired session
                return Response({"detail": "Session expired."}, status=status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_location(self, ip_address):
        try:
            response = requests.get(f'https://ipapi.co/{ip_address}/json/')
            data = response.json()
            return f"{data.get('city', '')}, {data.get('country_name', '')}"
        except:
            return None 