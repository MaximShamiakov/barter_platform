from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Ad(models.Model):
    CONDITION_CHOICES = [
        ('new', _('Новый')),
        ('used', _('Б/у')),
    ]

    CATEGORY_CHOICES = [
        ('electronics', _('Электроника')),
        ('clothing', _('Одежда')),
        ('books', _('Книги')),
        ('furniture', _('Мебель')),
        ('toys', _('Игрушки')),
        ('vehicles', _('Транспорт')),
        ('other', _('Другое')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name=_('Пользователь')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Заголовок'),
        help_text=_('Краткое описание товара')
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Подробное описание товара')
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('URL изображения'),
        help_text=_('Ссылка на изображение товара')
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name=_('Категория')
    )
    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        verbose_name=_('Состояние')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Объявление')
        verbose_name_plural = _('Объявления')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['condition']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для объявления"""
        return reverse('ads_list')

    def clean(self):
        """Валидация модели"""
        if self.title and len(self.title.strip()) < 3:
            raise ValidationError({
                'title': _('Заголовок должен содержать минимум 3 символа.')
            })
        if self.description and len(self.description.strip()) < 10:
            raise ValidationError({
                'description': _(
                    'Описание должно содержать минимум 10 символов.'
                )
            })


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидает')),
        ('accepted', _('Принята')),
        ('rejected', _('Отклонена')),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name=_('Объявление отправителя')
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name=_('Объявление получателя')
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_('Комментарий'),
        help_text=_('Дополнительная информация к предложению')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Статус')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    class Meta:
        verbose_name = _('Предложение обмена')
        verbose_name_plural = _('Предложения обмена')
        ordering = ['-created_at']
        unique_together = ['ad_sender', 'ad_receiver']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return (f'Обменять {self.ad_sender} на {self.ad_receiver} '
                f'[{self.status}]')

    def clean(self):
        """Валидация модели"""
        # Проверяем только если оба поля существуют и заполнены
        sender_id = self.ad_sender_id
        receiver_id = self.ad_receiver_id

        if sender_id is not None and receiver_id is not None:
            # Дополнительная проверка что объекты существуют
            if self.ad_sender and self.ad_receiver:
                if self.ad_sender == self.ad_receiver:
                    raise ValidationError(
                        _('Нельзя предложить обмен собственного товара '
                          'на себя же.')
                    )
                if self.ad_sender.user == self.ad_receiver.user:
                    raise ValidationError(
                        _('Нельзя предложить обмен между собственными '
                          'товарами.')
                    )

    @property
    def sender_user(self):
        """Возвращает пользователя-отправителя"""
        return self.ad_sender.user

    @property
    def receiver_user(self):
        """Возвращает пользователя-получателя"""
        return self.ad_receiver.user

    def can_be_updated_by(self, user):
        """Проверяет может ли пользователь обновить статус"""
        return user == self.receiver_user

    def accept(self):
        """Принять предложение"""
        self.status = 'accepted'
        self.save()

    def reject(self):
        """Отклонить предложение"""
        self.status = 'rejected'
        self.save()
