from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    """
    Configuration for the Users app.
    
    This app provides user management functionality including:
    - Extended user profiles
    - Session tracking and management
    - User authentication and authorization
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "User Management"

    def ready(self):
        """
        Initialize the app and register signals.
        
        This method is called when the app is ready, and is used to:
        1. Register signal handlers
        2. Set up any required initialization
        """
        logger.info("Initializing Users app")
        
        # Import signals to register them
        from . import signals
        logger.debug("Users app signals registered")
