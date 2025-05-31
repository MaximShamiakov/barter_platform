from django.urls import path
from .views_api import LoginView, AdListView, RegisterView, AdCreateAPIView, AdDeleteAPIView, AdUpdateAPIView, ExchangeProposalCreateView, UserReceivedProposalsListView, ExchangeProposalUpdateAPIView, UserSentProposalsListView


urlpatterns = [
    path('ad/', AdListView.as_view(), name='api_ads_list'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('ads/create/', AdCreateAPIView.as_view(), name='ad_create'),
    path('ads/<int:pk>/delete/', AdDeleteAPIView.as_view(), name='ad_delete'),
    path('ads/<int:pk>/update/', AdUpdateAPIView.as_view(), name='ad_update'),
    path('exchange/', ExchangeProposalCreateView.as_view(), name='exchange_create'),
    path('exchange_proposals/received/', UserReceivedProposalsListView.as_view(), name='received_proposals_list'),
    path('exchange_proposals/<int:pk>/update/', ExchangeProposalUpdateAPIView.as_view(), name='exchange_proposal_update'),
    path('exchange_proposals/sent/', UserSentProposalsListView.as_view(), name='user-sent-proposals'),
]