from django.urls import path
from .views_api import LoginView, AdListView, RegisterView, AdCreateAPIView, AdDeleteAPIView, AdUpdateAPIView, ExchangeProposalCreateView


urlpatterns = [
    path('ad/', AdListView.as_view(), name='api_ads_list'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('ads/create/', AdCreateAPIView.as_view(), name='ad_create'),
    path('ads/<int:pk>/delete/', AdDeleteAPIView.as_view(), name='ad_delete'),
    path('ads/<int:pk>/update/', AdUpdateAPIView.as_view(), name='ad_update'),
    path('api/exchange/', ExchangeProposalCreateView.as_view(), name='exchange-create')
]