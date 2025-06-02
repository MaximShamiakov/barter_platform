from rest_framework import serializers

from apps.ads.models import Ad


class UserSerializer(serializers.Serializer):
    """Базовый сериализатор для пользователя"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class AdListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка объявлений"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'category', 'condition',
            'created_at', 'user', 'image_url'
        ]


class AdSerializer(serializers.ModelSerializer):
    """Полный сериализатор для объявлений"""
    user = UserSerializer(read_only=True)
    received_proposals_count = serializers.SerializerMethodField()
    sent_proposals_count = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description', 'image_url', 'category',
            'condition', 'created_at', 'updated_at', 'user',
            'received_proposals_count', 'sent_proposals_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_received_proposals_count(self, obj):
        return obj.received_proposals.count()

    def get_sent_proposals_count(self, obj):
        return obj.sent_proposals.count()

    def create(self, validated_data):
        # Устанавливаем текущего пользователя как владельца
        request = self.context.get('request')
        if (request and hasattr(request, 'user') and
                request.user.is_authenticated):
            validated_data['user'] = request.user
        return super().create(validated_data)
