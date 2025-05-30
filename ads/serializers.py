from rest_framework import serializers
from .models import Ad

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
