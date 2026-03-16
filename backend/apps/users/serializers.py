from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    file_count = serializers.IntegerField(read_only=True)
    total_size = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'is_admin', 'storage_path', 'file_count', 'total_size']
        read_only_fields = ['storage_path', 'file_count', 'total_size']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password']

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
            raise serializers.ValidationError('Логин должен начинаться с буквы, содержать только латиницу и цифры, длина 4-20.')
        return value

    def validate_email(self, value):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise serializers.ValidationError('Неверный формат email.')
        return value

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        if not re.search(r'[!@#$%^&*()_+{}:"<>?]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы один специальный символ.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user