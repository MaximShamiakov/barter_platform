from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.ads.filters import AdFilter
from apps.ads.models import Ad

from .serializers import AdListSerializer, AdSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет редактировать объект только его владельцу.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Редактирование только для владельца
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(
        summary="Получить список объявлений",
        description=(
            "Возвращает список всех объявлений с возможностью фильтрации"
        ),
        tags=['Объявления']
    ),
    create=extend_schema(
        summary="Создать объявление",
        description="Создает новое объявление",
        tags=['Объявления']
    ),
    retrieve=extend_schema(
        summary="Получить объявление",
        description="Возвращает детальную информацию об объявлении",
        tags=['Объявления']
    ),
    update=extend_schema(
        summary="Обновить объявление",
        description="Обновляет объявление (полное обновление)",
        tags=['Объявления']
    ),
    partial_update=extend_schema(
        summary="Частично обновить объявление",
        description="Обновляет объявление (частичное обновление)",
        tags=['Объявления']
    ),
    destroy=extend_schema(
        summary="Удалить объявление",
        description="Удаляет объявление",
        tags=['Объявления']
    )
)
class AdViewSet(ModelViewSet):
    """
    ViewSet для объявлений с полным CRUD функционалом
    """
    queryset = Ad.objects.select_related('user').order_by('-created_at')
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = AdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return AdListSerializer
        return AdSerializer

    def get_queryset(self):
        """Фильтрация объявлений"""
        queryset = super().get_queryset()

        # Дополнительные фильтры
        category = self.request.query_params.get('category')
        condition = self.request.query_params.get('condition')
        user_id = self.request.query_params.get('user_id')

        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def get_permissions(self):
        """Настройка разрешений для разных действий"""
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @extend_schema(
        summary="Получить предложения для объявления",
        description=(
            "Возвращает все предложения обмена связанные с данным объявлением"
        ),
        tags=['Объявления'],
    )
    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        """Получить все предложения для объявления"""
        from api.proposals.serializers import ExchangeProposalSerializer

        ad = self.get_object()
        received_proposals = ad.received_proposals.select_related(
            'ad_sender__user', 'ad_receiver__user'
        )
        sent_proposals = ad.sent_proposals.select_related(
            'ad_sender__user', 'ad_receiver__user'
        )

        return Response({
            'received_proposals': ExchangeProposalSerializer(
                received_proposals, many=True, context={'request': request}
            ).data,
            'sent_proposals': ExchangeProposalSerializer(
                sent_proposals, many=True, context={'request': request}
            ).data
        })
