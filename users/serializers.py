from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

from .models import Users, Profile, UserSession


class PublicProfileSerializer(serializers.ModelSerializer):
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['is_available', 'badge', 'name', 'title', 'description', 'social_links']
        read_only_fields = fields  # All fields read-only for public view

    def get_social_links(self, obj):
        social_fields = [
            'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
            'hackerrank', 'medium', 'stackoverflow', 'portfolio',
            'youtube', 'devto'
        ]
        return {
            field: getattr(obj, field) 
            for field in social_fields 
            if getattr(obj, field) is not None
        }


class PublicUserSerializer(serializers.ModelSerializer):
    profile = PublicProfileSerializer(source='users.profile')

    class Meta:
        model = User
        fields = ['username', 'profile']
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'is_available', 'badge', 'name', 'title', 'description',
            'github', 'linkedin', 'twitter', 'facebook', 'leetcode',
            'hackerrank', 'medium', 'stackoverflow', 'portfolio',
            'youtube', 'devto'
        ]


class UsersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Users
        fields = ['profile', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    users = UsersSerializer()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'users']
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

    @transaction.atomic
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        profile_data = users_data.pop('profile')
        password = validated_data.pop('password')

        # Create User instance
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Profile is automatically created via signal
        # Update profile with provided data
        profile = user.users.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        users_data = validated_data.pop('users', None)

        # Update User fields
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Users and Profile fields
        if users_data and (profile_data := users_data.pop('profile', None)):
            profile = instance.users.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

            # Update any remaining Users fields
            for attr, value in users_data.items():
                setattr(instance.users, attr, value)
            instance.users.save()

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
