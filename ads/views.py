from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, AdFilterForm, AdForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal
from django.contrib.auth.decorators import login_required


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

    return render(request, 'ads/list.html', {
        'ads': ads_page,
        'form': form,
    })

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/create.html', {'form': form})

