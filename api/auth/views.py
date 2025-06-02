from django.contrib.auth import authenticate
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class LoginView(GenericAPIView):
    """
    API авторизации
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Авторизация пользователя",
        description=(
            "Авторизует пользователя и возвращает токен для доступа к API"
        ),
        tags=['Аутентификация']
    )
    def post(self, request):
        """Авторизация пользователя и возврат токена"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Получаем или создаем токен для пользователя
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(
                    user, context={'request': request}
                ).data,
                'detail': 'Авторизация успешна!'
            })
        else:
            return Response(
                {'detail': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(GenericAPIView):
    """
    API регистрации
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Регистрация нового пользователя",
        description=(
            "Регистрирует нового пользователя в системе и возвращает токен"
        ),
        tags=['Аутентификация']
    )
    def post(self, request):
        """Регистрация нового пользователя и возврат токена"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Используем транзакцию для обеспечения атомарности
        with transaction.atomic():
            user = serializer.save()
            token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(
                user, context={'request': request}
            ).data,
            'detail': 'Регистрация успешна!'
        }, status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):
    """
    API выхода из системы
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Выход из системы",
        description="Удаляет токен пользователя, тем самым завершая сессию",
        tags=['Аутентификация']
    )
    def post(self, request):
        """Выход из системы - удаление токена"""
        try:
            # Удаляем токен пользователя
            request.user.auth_token.delete()
            return Response({
                'detail': 'Выход выполнен успешно'
            })
        except Token.DoesNotExist:
            return Response({
                'detail': 'Токен не найден'
            }, status=status.HTTP_400_BAD_REQUEST)
