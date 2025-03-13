from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """Initialize app and setup logging"""
        logger.info("Initializing Users app")
        # Import signals to register them
        from . import signals
        logger.debug("Users app signals registered")
