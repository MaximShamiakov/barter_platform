from rest_framework import generics, permissions, status
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, LoginSerializer, RegisterSerializer, ExchangeProposalSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q


class AdListView(generics.ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self):
        queryset = Ad.objects.all().order_by('-created_at')

        search_query = self.request.query_params.get('search')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        condition = self.request.query_params.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset
    

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


class AdCreateAPIView(generics.CreateAPIView):
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Объявление успешно создано!',
            'ad': response.data
        }, status=status.HTTP_201_CREATED)


class AdDeleteAPIView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('Вы не можете удалять чужие объявления.')
        instance.delete()


class AdUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied('Вы не можете редактировать чужие объявления.')
        serializer.save()


class ExchangeProposalCreateView(generics.CreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request

        return context