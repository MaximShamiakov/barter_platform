from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Ad, ExchangeProposal
from .services import ValidationService


class AdFilterForm(forms.Form):
    q = forms.CharField(
        label=_('Поиск'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Поиск...')}),
    )

    category = forms.ChoiceField(
        label=_('Категория'),
        required=False,
        choices=[('', _('Все категории'))] + list(Ad.CATEGORY_CHOICES)
    )

    condition = forms.ChoiceField(
        label=_('Состояние'),
        required=False,
        choices=[('', _('Любое состояние'))] + list(Ad.CONDITION_CHOICES)
    )


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        labels = {
            'title': _('Название'),
            'description': _('Описание'),
            'image_url': _('Ссылка на изображение'),
            'category': _('Категория'),
            'condition': _('Состояние'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Введите название товара')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Подробное описание товара')
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        """ Валидация и очистка заголовка """
        title = self.cleaned_data.get('title')
        if title:
            title = ValidationService.sanitize_text(title, max_length=255)
            if len(title) < 3:
                raise ValidationError(
                    _('Заголовок должен содержать минимум 3 символа.')
                )
        return title

    def clean_description(self):
        """ Валидация и очистка описания """
        description = self.cleaned_data.get('description')
        if description:
            description = ValidationService.sanitize_text(description)
            if len(description) < 10:
                raise ValidationError(
                    _('Описание должно содержать минимум 10 символов.')
                )
        return description

    def clean_image_url(self):
        """ Валидация URL изображения """
        image_url = self.cleaned_data.get('image_url')
        if image_url:
            pass
        return image_url


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']
        widgets = {
            'ad_sender': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Дополнительная информация (необязательно)')
            }),
        }
        labels = {
            'ad_sender': _('Объявление отправителя'),
            'comment': _('Комментарий')
        }

    def clean_comment(self):
        """ Валидация и очистка комментария """
        comment = self.cleaned_data.get('comment')
        if comment:
            comment = ValidationService.sanitize_text(comment, max_length=500)
        return comment or ''


class ExchangeProposalFilterForm(forms.Form):
    STATUS_CHOICES = [('', _('Все'))] + list(ExchangeProposal.STATUS_CHOICES)

    FILTER_TYPE_CHOICES = [
        ('all', _('Все')),
        ('sent', _('Отправленные')),
        ('received', _('Полученные')),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label=_('Статус'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    filter_type = forms.ChoiceField(
        choices=FILTER_TYPE_CHOICES,
        required=False,
        label=_('Показывать'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
