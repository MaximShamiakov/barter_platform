"""
Сериализаторы для API пользователей версии 1
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для пользователя"""
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'ads_count'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'ads_count']

    def get_ads_count(self, obj):
        return obj.ads.count()

    def validate_email(self, value):
        """Проверяем уникальность email"""
        user = self.instance
        if (user and User.objects.filter(email=value)
                .exclude(pk=user.pk).exists()):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор профиля пользователя"""
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'ads_count'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'ads_count']

    def get_ads_count(self, obj):
        return obj.ads.count()
