from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, AdFilterForm, AdForm, ExchangeProposalForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def ads_list(request):
    form = AdFilterForm(request.GET)
    ads = Ad.objects.all().order_by('-created_at')

    if form.is_valid():
        query = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        condition = form.cleaned_data.get('condition')

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 10)
    page = request.GET.get('page')
    ads_page = paginator.get_page(page)
    get_params = request.GET.copy()
    get_params.pop('page', None)
    encoded_params = get_params.urlencode()

    return render(request, 'ads/list.html', {
        'ads': ads_page,
        'form': form,
        'querystring': encoded_params,
    })


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return render(request, 'ads/created.html', {'ad': ad})
    else:
        form = AdForm()
    return render(request, 'ads/create.html', {'form': form})


@login_required
def my_ads(request):
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ads/my_ads.html', {'ads': user_ads})


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('my_ads')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        ad.delete()

    return redirect('my_ads')


@login_required
def create_exchange_proposal(request):
    ad_receiver_id = request.GET.get('ad_receiver') or request.POST.get('ad_receiver')
    ad_receiver = get_object_or_404(Ad, id=ad_receiver_id)

    if request.method == 'POST':
        print("ad_sender из POST:", request.POST.get('ad_sender'))
        print(request)
        print(ad_receiver)
        form = ExchangeProposalForm(request.POST)
        form.fields['ad_sender'].queryset = Ad.objects.filter(user=request.user)
        if form.is_valid():
            exchange_proposal = form.save(commit=False)
            exchange_proposal.ad_receiver = ad_receiver
            exchange_proposal.save()
            return redirect('ads_list')

    else:
        form = ExchangeProposalForm()
        form.fields['ad_sender'].queryset = Ad.objects.filter(user=request.user)

    return render(request, 'exchange_proposals/create_exchange_proposal.html', {'form': form, 'ad_receiver': ad_receiver})


def custom_permission_denied_view(request, exception):
    return render(request, 'errors/403.html', status=403)


def custom_page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)

