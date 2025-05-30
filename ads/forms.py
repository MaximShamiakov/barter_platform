from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdFilterForm(forms.Form):
    q = forms.CharField(
        label = 'Поиск',
        required = False,
        widget = forms.TextInput(attrs={'placeholder': 'Поиск...'}),
    )

    category = forms.ChoiceField(
        label = 'Категория',
        required = False,
        choices = [('', 'Все категории')] + list(Ad.CATEGORY_CHOICES)
    )

    condition = forms.ChoiceField(
        label = 'Состояние',
        required = False,
        choices = [('', 'Любое состояние')] + list(Ad.CONDITION_CHOICES)
    )


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
            'condition': 'Состояние',
        }


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Необязательно'}),
        }
        labels = {
            'ad_sender': 'Объявление отправителя',
            'comment': 'Комментарий'
        }


class ExchangeProposalFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'Все')] + list(ExchangeProposal.STATUS_CHOICES)

    FILTER_TYPE_CHOICES = [
        ('all', 'Все'),
        ('sent', 'Отправленные'),
        ('received', 'Полученные'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Статус')
    filter_type = forms.ChoiceField(choices=FILTER_TYPE_CHOICES, required=False, label='Показывать')
