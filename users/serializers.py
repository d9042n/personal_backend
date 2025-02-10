from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Users, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['badge', 'name', 'title', 'description', 'github', 'linkedin', 'twitter']


class UsersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Users
        fields = ['profile', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    users = UsersSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'users']
        extra_kwargs = {
            'password': {'write_only': True}
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
