from django.urls import path
from .views_api import LoginView, AdListView


urlpatterns = [
    path('ad/', AdListView.as_view(), name='api_ads_list'),
    path('login/', LoginView.as_view(), name='api_login'),
]