from rest_framework import generics, serializers, permissions, status
from .models import Ad
from .serializers import AdSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.generics import GenericAPIView


class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer


class LoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def get(self, request):
        return Response(self.get_serializer().data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Вы успешно вошли!'})
        else:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def get(self, request):
        return Response(self.get_serializer().data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Пользователь успешно зарегистрирован!'}, status=status.HTTP_201_CREATED)
