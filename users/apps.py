from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """Initialize app and setup logging"""
        # Example of using info level logging
        logger.info("Initializing Users app")
        
        # Example of using warning level logging
        logger.warning("User app initialized with default settings - consider reviewing security configurations")
        
        # Import signals to register them
        from . import signals
        logger.debug("Users app signals registered")
