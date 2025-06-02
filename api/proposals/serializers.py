from rest_framework import serializers

from apps.ads.models import Ad, ExchangeProposal


class UserSerializer(serializers.Serializer):
    """Базовый сериализатор для пользователя"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class AdListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для объявлений"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'category', 'condition',
            'created_at', 'user', 'image_url'
        ]


class ExchangeProposalSerializer(serializers.ModelSerializer):
    """Сериализатор для предложений обмена"""
    ad_sender = AdListSerializer(read_only=True)
    ad_receiver = AdListSerializer(read_only=True)
    ad_sender_id = serializers.IntegerField(write_only=True)
    ad_receiver_id = serializers.IntegerField(write_only=True)
    sender_user = UserSerializer(read_only=True)
    receiver_user = UserSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver', 'ad_sender_id', 'ad_receiver_id',
            'comment', 'status', 'created_at', 'updated_at',
            'sender_user', 'receiver_user'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'sender_user', 'receiver_user'
        ]

    def validate(self, data):
        """Дополнительная валидация"""
        ad_sender_id = data.get('ad_sender_id')
        ad_receiver_id = data.get('ad_receiver_id')

        if ad_sender_id == ad_receiver_id:
            raise serializers.ValidationError(
                "Нельзя предложить обмен объявления на само себя"
            )

        # Проверяем существование объявлений
        try:
            ad_sender = Ad.objects.get(id=ad_sender_id)
            ad_receiver = Ad.objects.get(id=ad_receiver_id)
        except Ad.DoesNotExist:
            raise serializers.ValidationError(
                "Одно из объявлений не существует")

        # Проверяем что пользователь не обменивает свои объявления между собой
        if ad_sender.user == ad_receiver.user:
            raise serializers.ValidationError(
                "Нельзя предлагать обмен между собственными объявлениями"
            )

        # Проверяем что текущий пользователь является владельцем объявления-отправителя
        request = self.context.get('request')
        if request and request.user != ad_sender.user:
            raise serializers.ValidationError(
                "Вы можете предлагать обмен только от своих объявлений"
            )

        return data


class ExchangeProposalStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения статуса предложения"""

    class Meta:
        model = ExchangeProposal
        fields = ['status']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError(
                "Статус может быть только 'accepted' или 'rejected'"
            )
        return value
