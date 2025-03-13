import logging
from django.contrib.auth.models import User
from django.db import transaction

logger = logging.getLogger(__name__)

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
        logger.info(f"Creating new user with username: {username} and email: {email}")
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                **extra_fields
            )
            logger.debug(f"User created successfully with ID: {user.id}")

            # Update profile if data provided
            if profile_data:
                logger.debug(f"Updating profile for user {username} with data: {profile_data}")
                profile = user.users.profile
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
                logger.debug(f"Profile updated successfully for user {username}")

            logger.info(f"User {username} created successfully with complete profile")
            return user

        except Exception as e:
            logger.error(f"Error creating user {username}: {str(e)}", exc_info=True)
            raise

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
        logger.info(f"Updating profile for user: {user.username}")
        try:
            logger.debug(f"Profile update data: {profile_data}")
            profile = user.users.profile
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
            logger.info(f"Profile updated successfully for user: {user.username}")
            return profile
        except Exception as e:
            logger.error(f"Error updating profile for user {user.username}: {str(e)}", exc_info=True)
            raise
