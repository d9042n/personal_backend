from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone

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


class PublicProfileSerializer(serializers.ModelSerializer):
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['is_available', 'badge', 'name', 'title', 'description', 'social_links']
        read_only_fields = fields  # All fields read-only for public view

    def get_social_links(self, obj):
        social_fields = ['github', 'linkedin', 'twitter', 'facebook', 'leetcode', 
                        'hackerrank', 'medium', 'stackoverflow', 'portfolio', 
                        'youtube', 'devto']
        social_links = {field: getattr(obj, field) for field in social_fields}
        return {k: v for k, v in social_links.items() if v is not None}


class PublicUserSerializer(serializers.ModelSerializer):
    profile = PublicProfileSerializer(source='users.profile')

    class Meta:
        model = User
        fields = ['username', 'profile']
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_available', 'badge', 'name', 'title', 'description', 'github', 'linkedin', 'twitter']


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
        # Check if we should return limited fields for anonymous users
        if self.context.get('limited_fields'):
            return {
                'id': instance.id,
                'username': instance.username,
                # Add any other public fields you want to expose
            }
        return super().to_representation(instance)

    def create(self, validated_data):
        users_data = validated_data.pop('users')
        profile_data = users_data.pop('profile')

        # Create User instance
        password = validated_data.pop('password')
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

    def update(self, instance, validated_data):
        users_data = validated_data.pop('users', None)

        # Update User fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Update Users and Profile fields
        if users_data:
            users = instance.users
            profile_data = users_data.pop('profile', None)

            for attr, value in users_data.items():
                setattr(users, attr, value)
            users.save()

            if profile_data:
                profile = users.profile
                for attr, value in profile_data.items():
                    setattr(profile, attr, value)
                profile.save()

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
        return (obj.expires_at - timezone.now()).total_seconds()
