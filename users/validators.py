import re
from functools import partial
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import UserConstants


def validate_url_pattern(value, pattern, platform_name):
    """Generic URL validator for social media profiles"""
    if value and not re.match(pattern, value):
        raise ValidationError(_(f'Invalid {platform_name} URL format'))


# Create specific validators using partial application
validate_github_url = partial(
    validate_url_pattern,
    pattern=UserConstants.GITHUB_URL_PATTERN,
    platform_name='GitHub'
)

validate_linkedin_url = partial(
    validate_url_pattern,
    pattern=UserConstants.LINKEDIN_URL_PATTERN,
    platform_name='LinkedIn'
)

validate_twitter_url = partial(
    validate_url_pattern,
    pattern=UserConstants.TWITTER_URL_PATTERN,
    platform_name='Twitter'
)

validate_facebook_url = partial(
    validate_url_pattern,
    pattern=UserConstants.FACEBOOK_URL_PATTERN,
    platform_name='Facebook'
)

validate_leetcode_url = partial(
    validate_url_pattern,
    pattern=UserConstants.LEETCODE_URL_PATTERN,
    platform_name='LeetCode'
)

validate_hackerrank_url = partial(
    validate_url_pattern,
    pattern=UserConstants.HACKERRANK_URL_PATTERN,
    platform_name='HackerRank'
)

validate_medium_url = partial(
    validate_url_pattern,
    pattern=UserConstants.MEDIUM_URL_PATTERN,
    platform_name='Medium'
)

validate_stackoverflow_url = partial(
    validate_url_pattern,
    pattern=UserConstants.STACKOVERFLOW_URL_PATTERN,
    platform_name='Stack Overflow'
)

validate_portfolio_url = partial(
    validate_url_pattern,
    pattern=UserConstants.PORTFOLIO_URL_PATTERN,
    platform_name='Portfolio'
)

validate_youtube_url = partial(
    validate_url_pattern,
    pattern=UserConstants.YOUTUBE_URL_PATTERN,
    platform_name='YouTube'
)

validate_devto_url = partial(
    validate_url_pattern,
    pattern=UserConstants.DEVTO_URL_PATTERN,
    platform_name='Dev.to'
)
