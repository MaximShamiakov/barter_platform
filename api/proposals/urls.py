from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExchangeProposalViewSet

app_name = 'proposals'

router = DefaultRouter()
router.register(r'', ExchangeProposalViewSet, basename='proposal')

urlpatterns = [
    path('', include(router.urls)),
]
