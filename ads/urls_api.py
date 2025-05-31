from django.urls import path
from .views_api import LoginView, AdListView, RegisterView, AdListCreateAPIView,AdDeleteAPIView


urlpatterns = [
    path('ad/', AdListView.as_view(), name='api_ads_list'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('ads/', AdListCreateAPIView.as_view(), name='ad-list-create'),
    path('ads/<int:pk>/delete/', AdDeleteAPIView.as_view(), name='ad-delete'),
]