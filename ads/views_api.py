from rest_framework import generics, permissions, status
from .models import Ad
from .serializers import AdSerializer, LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import PermissionDenied



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


class AdListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdDeleteAPIView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('Вы не можете удалять чужие объявления.')
        instance.delete()
