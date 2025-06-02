import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import (AdFilterForm, AdForm, ExchangeProposalFilterForm,
                    ExchangeProposalForm)
from .models import Ad, ExchangeProposal
from .services import AdService, ExchangeProposalService

logger = logging.getLogger(__name__)


def get_filtered_paginated_ads(request, ads_queryset):
    form = AdFilterForm(request.GET)

    query = None
    category = None
    condition = None

    if form.is_valid():
        query = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        condition = form.cleaned_data.get('condition')

    if query:
        ads_queryset = ads_queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads_queryset = ads_queryset.filter(category=category)
    if condition:
        ads_queryset = ads_queryset.filter(condition=condition)

    paginator = Paginator(ads_queryset, 10)
    page = request.GET.get('page')
    ads_page = paginator.get_page(page)
    get_params = request.GET.copy()
    get_params.pop('page', None)
    encoded_params = get_params.urlencode()

    return ads_page, form, encoded_params


def ads_list(request):
    """Отображение списка всех объявлений с фильтрацией и пагинацией."""
    exclude_user = request.user if request.user.is_authenticated else None
    ads = AdService.search_ads(exclude_user=exclude_user)
    ads_page, form, querystring = get_filtered_paginated_ads(request, ads)

    return render(request, 'ads/list.html', {
        'ads': ads_page,
        'form': form,
        'querystring': querystring,
    })


@login_required
def my_ads(request):
    """Отображение объявлений пользователя с фильтрацией и пагинацией."""
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    ads_page, form, querystring = get_filtered_paginated_ads(request, user_ads)
    return render(request, 'ads/my_ads.html', {
        'ads': ads_page,
        'form': form,
        'querystring': querystring,
    })


@login_required
def create_ad(request):
    """Создание нового объявления."""
    if request.method == 'POST':
        form = AdForm(request.POST)

        if form.is_valid():
            try:
                ad = AdService.create_ad(
                    user=request.user,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    condition=form.cleaned_data['condition'],
                    image_url=form.cleaned_data.get('image_url')
                )
                messages.success(request, _('Объявление успешно создано!'))
                return render(request, 'ads/created.html', {'ad': ad})
            except ValidationError as e:
                logger.warning(
                    f"Ad creation failed for user {request.user.username}: {e}"
                )
                messages.error(
                    request,
                    _('Ошибка при создании объявления: {}').format(e)
                )
    else:
        form = AdForm()
    return render(request, 'ads/create.html', {'form': form})


@login_required
def edit_ad(request, ad_id):
    """Редактирование существующего объявления."""
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            try:
                AdService.update_ad(
                    ad=ad,
                    user=request.user,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    condition=form.cleaned_data['condition'],
                    image_url=form.cleaned_data.get('image_url')
                )
                messages.success(request, _('Объявление успешно обновлено!'))
                return redirect('my_ads')
            except (ValidationError, PermissionError) as e:
                logger.warning(
                    f"Ad update failed for user {request.user.username}: {e}")
                messages.error(
                    request,
                    _('Ошибка при обновлении объявления: {}').format(e)
                )
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    """Удаление объявления с использованием слоя сервиса."""
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        try:
            AdService.delete_ad(ad=ad, user=request.user)
            messages.success(request, _('Объявление успешно удалено!'))
        except PermissionError as e:
            logger.warning(
                f"Ad deletion failed for user {request.user.username}: {e}")
            messages.error(
                request,
                _('У вас нет прав для удаления этого объявления.')
            )

    return redirect('my_ads')


@login_required
@transaction.atomic
def create_exchange_proposal(request):
    """Создание предложения обмена с использованием слоя сервиса."""
    ad_receiver_id = request.GET.get(
        'ad_receiver') or request.POST.get('ad_receiver')
    ad_receiver = get_object_or_404(Ad, id=ad_receiver_id)

    if ad_receiver.user == request.user:
        messages.error(
            request,
            _('Вы не можете предложить обмен с собственным объявлением.')
        )
        return redirect('ads_list')

    user_ads = Ad.objects.filter(user=request.user)
    if not user_ads.exists():
        messages.error(
            request,
            _('У вас нет объявлений для обмена. Создайте объявление сначала.')
        )
        return redirect('create_ad')

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        form.fields['ad_sender'].queryset = user_ads
        if form.is_valid():
            try:
                ExchangeProposalService.create_proposal(
                    sender_user=request.user,
                    ad_sender=form.cleaned_data['ad_sender'],
                    ad_receiver=ad_receiver,
                    comment=form.cleaned_data.get('comment', '')
                )
                messages.success(request, _('Предложение обмена отправлено!'))
                return redirect('ads_list')
            except ValidationError as e:
                logger.warning(f"Exchange proposal creation failed: {e}")
                messages.error(request, str(e))
    else:
        form = ExchangeProposalForm()
        form.fields['ad_sender'].queryset = user_ads

    return render(request, 'exchange_proposals/create_exchange_proposal.html',
                  {'form': form, 'ad_receiver': ad_receiver})


@login_required
def exchange_proposals_list(request):
    """Отображение списка предложений обмена с использованием слоя сервиса."""
    form = ExchangeProposalFilterForm(request.GET or None)

    filter_type = 'all'
    status_filter = None

    if form.is_valid():
        status_filter = form.cleaned_data.get('status')
        filter_type = form.cleaned_data.get('filter_type') or 'all'

    sent_proposals, received_proposals = (
        ExchangeProposalService.get_user_proposals(
            user=request.user,
            filter_type=filter_type,
            status=status_filter
        )
    )

    context = {
        'form': form,
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
    }

    return render(request, 'exchange_proposals/exchange_proposals_list.html',
                  context)


@login_required
@transaction.atomic
def update_proposal_status(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'accept':
                ExchangeProposalService.update_proposal_status(
                    proposal=proposal,
                    user=request.user,
                    status='accepted'
                )
                messages.success(request, _('Предложение принято!'))
            elif action == 'reject':
                ExchangeProposalService.update_proposal_status(
                    proposal=proposal,
                    user=request.user,
                    status='rejected'
                )
                messages.success(request, _('Предложение отклонено!'))
            else:
                messages.warning(request, _('Неверное действие.'))
        except (PermissionError, ValidationError) as e:
            logger.warning(f"Proposal status update failed: {e}")
            messages.error(request, str(e))

    return redirect('exchange_proposals_list')


def custom_permission_denied_view(request, exception):
    logger.warning(f"Permission denied for user {request.user}: {exception}")
    return render(request, 'errors/403.html', status=403)


def custom_page_not_found_view(request, exception):
    logger.info(f"Page not found: {request.path}")
    return render(request, 'errors/404.html', status=404)


def custom_bad_request_view(request, exception):
    logger.warning(
        f"Bad request from {request.META.get('REMOTE_ADDR')}: {request.path}")
    return render(request, 'errors/400.html', status=400)


def custom_server_error_view(request):
    logger.error(f"Server error on {request.path}")
    return render(request, 'errors/500.html', status=500)
