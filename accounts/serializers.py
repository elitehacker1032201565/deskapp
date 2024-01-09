# serializers.py
import random
from rest_framework import serializers
from .models import CustomUser, UploadedFile
from djoser.serializers import TokenCreateSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'public_visibility', 'is_active', 'is_staff', 'date_joined','is_verified']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'user', 'title', 'description', 'file', 'visibility', 'cost', 'year_published']


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class CustomTokenCreateSerializer(TokenCreateSerializer):
    
    pass