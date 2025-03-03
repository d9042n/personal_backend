from django.utils.translation import gettext_lazy as _
from typing import Dict, List, Tuple, Pattern
import re


class UserConstants:
    """Constants for user-related functionality.
    
    This class contains all constants related to user profiles, badges,
    and social media URL validation patterns.
    """

    # Profile Badge Types
    class Badges:
        """Available badge types for user profiles."""
        AVAILABLE = 'available'
        BUSY = 'busy'
        OFFLINE = 'offline'

        CHOICES: List[Tuple[str, str]] = [
            (AVAILABLE, _('Available for hire')),
            (BUSY, _('Currently busy')),
            (OFFLINE, _('Not available')),
        ]

    # Profile Title Defaults
    DEFAULT_TITLE = ''

    # Social Media URL Patterns
    class URLPatterns:
        """Regular expression patterns for validating social media profile URLs.
        
        Each pattern is compiled once at module load for better performance.
        All patterns are case-insensitive and support both http and https.
        """
        # Common URL components
        PROTOCOL = r'https?://(?:www\.)?'
        USERNAME = r'[\w-]+'
        OPTIONAL_SLASH = r'/?$'

        # Platform-specific patterns
        GITHUB = re.compile(
            f'^{PROTOCOL}github\.com/{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        LINKEDIN = re.compile(
            f'^{PROTOCOL}linkedin\.com/in/{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        TWITTER = re.compile(
            f'^{PROTOCOL}twitter\.com/{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        FACEBOOK = re.compile(
            f'^{PROTOCOL}facebook\.com/[\w\.-]+{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        LEETCODE = re.compile(
            f'^{PROTOCOL}leetcode\.com/(?:u/)?{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        HACKERRANK = re.compile(
            f'^{PROTOCOL}hackerrank\.com/(?:profile/)?{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        MEDIUM = re.compile(
            f'^{PROTOCOL}medium\.com/@?{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        STACKOVERFLOW = re.compile(
            f'^{PROTOCOL}stackoverflow\.com/users/[\d-]+/{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        PORTFOLIO = re.compile(
            f'^{PROTOCOL}[\w\.-]+\.\w+/?.*$',
            re.IGNORECASE
        )
        
        YOUTUBE = re.compile(
            f'^{PROTOCOL}youtube\.com/(?:c/|channel/|@)?{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )
        
        DEVTO = re.compile(
            f'^{PROTOCOL}dev\.to/{USERNAME}{OPTIONAL_SLASH}',
            re.IGNORECASE
        )

    # For backward compatibility
    BADGE_AVAILABLE = Badges.AVAILABLE
    BADGE_BUSY = Badges.BUSY
    BADGE_OFFLINE = Badges.OFFLINE
    BADGE_CHOICES = Badges.CHOICES

    GITHUB_URL_PATTERN = URLPatterns.GITHUB.pattern
    LINKEDIN_URL_PATTERN = URLPatterns.LINKEDIN.pattern
    TWITTER_URL_PATTERN = URLPatterns.TWITTER.pattern
    FACEBOOK_URL_PATTERN = URLPatterns.FACEBOOK.pattern
    LEETCODE_URL_PATTERN = URLPatterns.LEETCODE.pattern
    HACKERRANK_URL_PATTERN = URLPatterns.HACKERRANK.pattern
    MEDIUM_URL_PATTERN = URLPatterns.MEDIUM.pattern
    STACKOVERFLOW_URL_PATTERN = URLPatterns.STACKOVERFLOW.pattern
    PORTFOLIO_URL_PATTERN = URLPatterns.PORTFOLIO.pattern
    YOUTUBE_URL_PATTERN = URLPatterns.YOUTUBE.pattern
    DEVTO_URL_PATTERN = URLPatterns.DEVTO.pattern
