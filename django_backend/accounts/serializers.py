from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import forms
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source='gender.name')
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'is_active',
            'created_at',
        )

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = UserCreateSerializer.Meta.fields + ('profile_picture',)


    
