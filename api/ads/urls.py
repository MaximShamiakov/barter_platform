from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdViewSet

app_name = 'ads'

router = DefaultRouter()
router.register(r'', AdViewSet, basename='ad')

urlpatterns = [
    path('', include(router.urls)),
]
