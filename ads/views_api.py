from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad
from .serializers import AdsSerializer

class AdsListView(generics.ListAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdsSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'condition']
