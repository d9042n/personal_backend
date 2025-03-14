import re
from functools import partial
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import UserConstants


def validate_url_pattern(value, pattern, platform_name):
    """
    Generic URL validator for social media profiles.
    
    Args:
        value (str): The URL to validate
        pattern (str): Regular expression pattern to match against
        platform_name (str): Name of the platform for error messages
        
    Raises:
        ValidationError: If the URL format is invalid for the given platform
    """
    if value and not re.match(pattern, value):
        raise ValidationError(_(f'Invalid {platform_name} URL format'))


# Platform-specific validators using partial application
validate_github_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.GITHUB.pattern,
    platform_name='GitHub'
)

validate_linkedin_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.LINKEDIN.pattern,
    platform_name='LinkedIn'
)

validate_twitter_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.TWITTER.pattern,
    platform_name='Twitter'
)

validate_facebook_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.FACEBOOK.pattern,
    platform_name='Facebook'
)

validate_leetcode_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.LEETCODE.pattern,
    platform_name='LeetCode'
)

validate_hackerrank_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.HACKERRANK.pattern,
    platform_name='HackerRank'
)

validate_medium_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.MEDIUM.pattern,
    platform_name='Medium'
)

validate_stackoverflow_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.STACKOVERFLOW.pattern,
    platform_name='Stack Overflow'
)

validate_portfolio_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.PORTFOLIO.pattern,
    platform_name='Portfolio'
)

validate_youtube_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.YOUTUBE.pattern,
    platform_name='YouTube'
)

validate_devto_url = partial(
    validate_url_pattern,
    pattern=UserConstants.URLPatterns.DEVTO.pattern,
    platform_name='Dev.to'
)

# Add docstrings to each validator
validate_github_url.__doc__ = "Validate GitHub profile URL format"
validate_linkedin_url.__doc__ = "Validate LinkedIn profile URL format"
validate_twitter_url.__doc__ = "Validate Twitter profile URL format"
validate_facebook_url.__doc__ = "Validate Facebook profile URL format"
validate_leetcode_url.__doc__ = "Validate LeetCode profile URL format"
validate_hackerrank_url.__doc__ = "Validate HackerRank profile URL format"
validate_medium_url.__doc__ = "Validate Medium profile URL format"
validate_stackoverflow_url.__doc__ = "Validate Stack Overflow profile URL format"
validate_portfolio_url.__doc__ = "Validate portfolio website URL format"
validate_youtube_url.__doc__ = "Validate YouTube channel URL format"
validate_devto_url.__doc__ = "Validate Dev.to profile URL format"
