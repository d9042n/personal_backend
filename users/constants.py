from django.utils.translation import gettext_lazy as _


class UserConstants:
    """Constants for user-related functionality"""

    # Profile Badge Types
    BADGE_AVAILABLE = 'available'
    BADGE_BUSY = 'busy'
    BADGE_OFFLINE = 'offline'

    BADGE_CHOICES = [
        (BADGE_AVAILABLE, _('Available for hire')),
        (BADGE_BUSY, _('Currently busy')),
        (BADGE_OFFLINE, _('Not available')),
    ]

    # Profile Title Defaults
    DEFAULT_TITLE = ''

    # Social Media URL Patterns
    GITHUB_URL_PATTERN = r'^https?://(?:www\.)?github\.com/[\w-]+/?$'
    LINKEDIN_URL_PATTERN = r'^https?://(?:www\.)?linkedin\.com/in/[\w-]+/?$'
    TWITTER_URL_PATTERN = r'^https?://(?:www\.)?twitter\.com/[\w-]+/?$'
