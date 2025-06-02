from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.ads.filters import ExchangeProposalFilter
from apps.ads.models import ExchangeProposal

from .serializers import (ExchangeProposalSerializer,
                          ExchangeProposalStatusSerializer)


class IsProposalParticipant(permissions.BasePermission):
    """
    Разрешение для участников предложения обмена.
    """

    def has_object_permission(self, request, view, obj):
        # Участники: отправитель и получатель
        return (request.user == obj.sender_user or
                request.user == obj.receiver_user)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список предложений обмена",
        description="Возвращает список предложений обмена пользователя",
        tags=['Предложения обмена']
    ),
    create=extend_schema(
        summary="Создать предложение обмена",
        description="Создает новое предложение обмена",
        tags=['Предложения обмена']
    ),
    retrieve=extend_schema(
        summary="Получить предложение обмена",
        description="Возвращает детальную информацию о предложении обмена",
        tags=['Предложения обмена']
    ),
    update=extend_schema(
        summary="Обновить предложение обмена",
        description="Обновляет предложение обмена (полное обновление)",
        tags=['Предложения обмена']
    ),
    partial_update=extend_schema(
        summary="Частично обновить предложение обмена",
        description="Обновляет предложение обмена (частичное обновление)",
        tags=['Предложения обмена']
    ),
    destroy=extend_schema(
        summary="Удалить предложение обмена",
        description="Удаляет предложение обмена",
        tags=['Предложения обмена']
    )
)
class ExchangeProposalViewSet(ModelViewSet):
    """
    ViewSet для предложений обмена
    """
    queryset = ExchangeProposal.objects.select_related(
        'ad_sender__user', 'ad_receiver__user'
    ).order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated, IsProposalParticipant]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ExchangeProposalFilter
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Показывать только предложения пользователя"""
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(
                Q(ad_sender__user=user) | Q(ad_receiver__user=user)
            )
        return self.queryset.none()

    def get_permissions(self):
        """Настройка разрешений для разных действий"""
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsProposalParticipant]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @extend_schema(
        summary="Изменить статус предложения",
        description=(
            "Позволяет получателю предложения изменить его статус"
        ),
        tags=['Предложения обмена'],
        request=ExchangeProposalStatusSerializer,
        responses={200: ExchangeProposalSerializer}
    )
    @action(detail=True, methods=['patch'],
            serializer_class=ExchangeProposalStatusSerializer)
    def update_status(self, request, pk=None):
        """Изменить статус предложения (только получатель)"""
        proposal = self.get_object()

        # Только получатель может изменять статус
        if request.user != proposal.receiver_user:
            return Response(
                {
                    'detail': (
                        'Только получатель может изменить статус предложения'
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            proposal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            ExchangeProposalSerializer(
                proposal, context={'request': request}).data
        )
