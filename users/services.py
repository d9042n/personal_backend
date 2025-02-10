from django.contrib.auth.models import User
from django.db import transaction
from .models import Users, Profile

class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(username, email, password, profile_data=None, **extra_fields):
        """
        Create a new user with profile
        
        Args:
            username: Username for new user
            email: Email address
            password: Password
            profile_data: Dictionary of profile data
            **extra_fields: Additional User model fields
            
        Returns:
            Created User instance
        """
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        
        # Update profile if data provided
        if profile_data:
            profile = user.users.profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
            
        return user
    
    @staticmethod
    @transaction.atomic
    def update_user_profile(user, profile_data):
        """
        Update user profile
        
        Args:
            user: User instance
            profile_data: Dictionary of profile data to update
            
        Returns:
            Updated Profile instance
        """
        profile = user.users.profile
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        return profile 