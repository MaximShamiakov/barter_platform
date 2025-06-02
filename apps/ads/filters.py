import django_filters
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Ad, ExchangeProposal


class AdFilter(django_filters.FilterSet):
    """Фильтр для объявлений"""
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск в заголовке'
    )
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Поиск в описании'
    )
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск по заголовку и описанию'
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Пользователь'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Создано после'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Создано до'
    )

    class Meta:
        model = Ad
        fields = {
            'category': ['exact', 'in'],
            'condition': ['exact', 'in'],
        }

    def filter_search(self, queryset, name, value):
        """Поиск по заголовку и описанию"""
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
        return queryset


class ExchangeProposalFilter(django_filters.FilterSet):
    """Фильтр для предложений обмена"""
    status = django_filters.ChoiceFilter(
        choices=ExchangeProposal.STATUS_CHOICES,
        label='Статус'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Создано после'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Создано до'
    )
    ad_sender_category = django_filters.CharFilter(
        field_name='ad_sender__category',
        lookup_expr='exact',
        label='Категория предлагаемого товара'
    )
    ad_receiver_category = django_filters.CharFilter(
        field_name='ad_receiver__category',
        lookup_expr='exact',
        label='Категория желаемого товара'
    )

    class Meta:
        model = ExchangeProposal
        fields = ['status']
