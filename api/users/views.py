from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserProfileSerializer, UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Получить список пользователей",
        description="Возвращает список всех пользователей",
        tags=['Пользователи']
    ),
    create=extend_schema(
        summary="Создать пользователя",
        description="Создает нового пользователя",
        tags=['Пользователи']
    ),
    retrieve=extend_schema(
        summary="Получить пользователя",
        description="Возвращает информацию о пользователе",
        tags=['Пользователи']
    ),
    update=extend_schema(
        summary="Обновить пользователя",
        description="Обновляет пользователя (полное обновление)",
        tags=['Пользователи']
    ),
    partial_update=extend_schema(
        summary="Частично обновить пользователя",
        description="Обновляет пользователя (частичное обновление)",
        tags=['Пользователи']
    ),
    destroy=extend_schema(
        summary="Удалить пользователя",
        description="Удаляет пользователя",
        tags=['Пользователи']
    )
)
class UserViewSet(ModelViewSet):
    """
    ViewSet для пользователей
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']

    def get_permissions(self):
        """Настройка разрешений для разных действий"""
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        """Переопределяем для защиты приватных данных"""
        obj = super().get_object()
        if (self.action in ['update', 'partial_update', 'destroy']
                and self.request.user != obj):
            self.permission_denied(
                self.request,
                message='Вы можете редактировать только свой профиль'
            )
        return obj

    @extend_schema(
        summary="Получить профиль текущего пользователя",
        description=(
            "Возвращает расширенную информацию о текущем пользователе"
        ),
        tags=['Пользователи'],
        responses={200: UserProfileSerializer}
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Получить профиль текущего пользователя"""
        serializer = UserProfileSerializer(
            request.user, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        summary="Обновить профиль текущего пользователя",
        description="Позволяет пользователю обновить свой профиль",
        tags=['Пользователи'],
        request=UserSerializer,
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['patch'],
            permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Обновить профиль текущего пользователя"""
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Удалить аккаунт пользователя",
        description="Полностью удаляет аккаунт текущего пользователя",
        tags=['Пользователи'],
        responses={204: None}
    )
    @action(detail=False, methods=['delete'],
            permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        """Удалить аккаунт пользователя"""
        user = request.user
        user.delete()
        return Response(status=204)
