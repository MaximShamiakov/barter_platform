from rest_framework import serializers
from .models import Ad, ExchangeProposal
from django.contrib.auth.models import User


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['user']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают.')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'comment', 'status', 'created_at']
        read_only_fields = ['created_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
            self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)
            

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        return super().create(validated_data)
