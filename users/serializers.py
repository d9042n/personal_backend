from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

from .models import Users, Profile, UserSession


class SocialLinksSerializer(serializers.Serializer):
    github = serializers.URLField(required=False, allow_null=True)
    linkedin = serializers.URLField(required=False, allow_null=True)
    twitter = serializers.URLField(required=False, allow_null=True)
    facebook = serializers.URLField(required=False, allow_null=True)
    leetcode = serializers.URLField(required=False, allow_null=True)
    hackerrank = serializers.URLField(required=False, allow_null=True)
    medium = serializers.URLField(required=False, allow_null=True)
    stackoverflow = serializers.URLField(required=False, allow_null=True)
    portfolio = serializers.URLField(required=False, allow_null=True)
    youtube = serializers.URLField(required=False, allow_null=True)
    devto = serializers.URLField(required=False, allow_null=True)


class ProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinksSerializer(required=False)

    class Meta:
        model = Profile
        fields = [
            'is_available', 'badge', 'name', 'title', 'description',
            'social_links'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        social_fields = [
            'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
            'hackerrank', 'medium', 'stackoverflow', 'portfolio',
            'youtube', 'devto'
        ]
        social_links = {}
        for field in social_fields:
            value = getattr(instance, field)
            if value:  # Only include non-null and non-empty values
                social_links[field] = value
        ret['social_links'] = social_links
        return ret

    def _update_social_links(self, instance, social_links):
        """Helper method to update social links"""
        if social_links:
            social_fields = [
                'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
                'hackerrank', 'medium', 'stackoverflow', 'portfolio',
                'youtube', 'devto'
            ]
            for field in social_fields:
                if field in social_links:
                    setattr(instance, field, social_links.get(field))

    def update(self, instance, validated_data):
        social_links = validated_data.pop('social_links', None)
        
        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update social links if provided
        if social_links:
            self._update_social_links(instance, social_links)
        
        instance.save()
        return instance


class PublicProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        read_only_fields = fields = ProfileSerializer.Meta.fields


class PublicUserSerializer(serializers.ModelSerializer):
    profile = PublicProfileSerializer(source='users.profile')

    class Meta:
        model = User
        fields = ['username', 'profile']
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='users.profile')
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def to_representation(self, instance):
        if self.context.get('limited_fields'):
            return {
                'id': instance.id,
                'username': instance.username
            }
        return super().to_representation(instance)

    def _update_profile(self, profile, profile_data):
        """Helper method to update profile"""
        if not profile_data:
            return

        social_links = profile_data.pop('social_links', None)
        
        # Update regular profile fields
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        
        # Update social links if provided
        if social_links:
            social_fields = [
                'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
                'hackerrank', 'medium', 'stackoverflow', 'portfolio',
                'youtube', 'devto'
            ]
            for field in social_fields:
                if field in social_links:
                    setattr(profile, field, social_links.get(field))
        
        profile.save()

    @transaction.atomic
    def create(self, validated_data):
        profile_data = None
        if 'users' in validated_data:
            profile_data = validated_data.pop('users', {}).get('profile', {})
        elif 'profile' in validated_data:
            profile_data = validated_data.pop('profile', {})
            
        password = validated_data.pop('password')

        # Create User instance
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Profile is automatically created via signal
        # Update profile with provided data
        if profile_data:
            self._update_profile(user.users.profile, profile_data)

        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = None
        if 'users' in validated_data:
            profile_data = validated_data.pop('users', {}).get('profile', {})
        elif 'profile' in validated_data:
            profile_data = validated_data.pop('profile', {})

        # Update User fields
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        self._update_profile(instance.users.profile, profile_data)

        return instance


class UserSessionSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    time_until_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'created_at', 'last_activity', 
            'ip_address', 'user_agent', 'device_type', 'location',
            'is_active', 'expires_at', 'duration', 'time_until_expiry'
        ]
        read_only_fields = fields

    def get_duration(self, obj):
        return (obj.last_activity - obj.created_at).total_seconds()

    def get_time_until_expiry(self, obj):
        if obj.is_expired():
            return 0
        return max(0, (obj.expires_at - timezone.now()).total_seconds())
