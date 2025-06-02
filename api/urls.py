"""
Главные URL маршруты для API без версионирования
"""
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

app_name = 'api'

urlpatterns = [
    # Объявления
    path('ads/', include('api.ads.urls')),

    # Пользователи
    path('users/', include('api.users.urls')),

    # Предложения обмена
    path('proposals/', include('api.proposals.urls')),

    # Аутентификация
    path('auth/', include('api.auth.urls')),

    # Документация API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'),
         name='swagger-ui'),
]
