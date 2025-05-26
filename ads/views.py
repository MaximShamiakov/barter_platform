# ads/views.py
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Вы можете войти.')
            return redirect('login')  # можно поменять на любую страницу
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
