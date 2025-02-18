import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import UserConstants


def validate_github_url(value):
    """Validate GitHub profile URL format"""
    if value and not re.match(UserConstants.GITHUB_URL_PATTERN, value):
        raise ValidationError(_('Invalid GitHub URL format'))


def validate_linkedin_url(value):
    """Validate LinkedIn profile URL format"""
    if value and not re.match(UserConstants.LINKEDIN_URL_PATTERN, value):
        raise ValidationError(_('Invalid LinkedIn URL format'))


def validate_twitter_url(value):
    """Validate Twitter profile URL format"""
    if value and not re.match(UserConstants.TWITTER_URL_PATTERN, value):
        raise ValidationError(_('Invalid Twitter URL format'))


def validate_facebook_url(value):
    """Validate Facebook profile URL format"""
    if value and not re.match(UserConstants.FACEBOOK_URL_PATTERN, value):
        raise ValidationError(_('Invalid Facebook URL format'))


def validate_leetcode_url(value):
    """Validate LeetCode profile URL format"""
    if value and not re.match(UserConstants.LEETCODE_URL_PATTERN, value):
        raise ValidationError(_('Invalid LeetCode URL format'))


def validate_hackerrank_url(value):
    """Validate HackerRank profile URL format"""
    if value and not re.match(UserConstants.HACKERRANK_URL_PATTERN, value):
        raise ValidationError(_('Invalid HackerRank URL format'))


def validate_medium_url(value):
    """Validate Medium profile URL format"""
    if value and not re.match(UserConstants.MEDIUM_URL_PATTERN, value):
        raise ValidationError(_('Invalid Medium URL format'))


def validate_stackoverflow_url(value):
    """Validate Stack Overflow profile URL format"""
    if value and not re.match(UserConstants.STACKOVERFLOW_URL_PATTERN, value):
        raise ValidationError(_('Invalid Stack Overflow URL format'))


def validate_portfolio_url(value):
    """Validate personal portfolio URL format"""
    if value and not re.match(UserConstants.PORTFOLIO_URL_PATTERN, value):
        raise ValidationError(_('Invalid portfolio URL format'))


def validate_youtube_url(value):
    """Validate YouTube channel URL format"""
    if value and not re.match(UserConstants.YOUTUBE_URL_PATTERN, value):
        raise ValidationError(_('Invalid YouTube URL format'))


def validate_devto_url(value):
    """Validate Dev.to profile URL format"""
    if value and not re.match(UserConstants.DEVTO_URL_PATTERN, value):
        raise ValidationError(_('Invalid Dev.to URL format'))
