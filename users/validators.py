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
