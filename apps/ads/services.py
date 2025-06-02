import logging
from typing import Optional, Tuple

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q, QuerySet

from .models import Ad, ExchangeProposal

logger = logging.getLogger(__name__)


class AdService:
    """Класс сервиса для бизнес-логики объявлений"""

    @staticmethod
    def create_ad(user: User, title: str, description: str,
                  category: str, condition: str,
                  image_url: Optional[str] = None) -> Ad:
        logger.info(f"Creating ad for user {user.username}: {title}")

        with transaction.atomic():
            ad = Ad(
                user=user,
                title=title.strip(),
                description=description.strip(),
                category=category,
                condition=condition,
                image_url=image_url
            )
            ad.full_clean()  # Run model validation
            ad.save()

        logger.info(f"Ad created successfully with ID: {ad.id}")
        return ad

    @staticmethod
    def update_ad(ad: Ad, user: User, **kwargs) -> Ad:
        """ Обновление существующего объявления """

        if ad.user != user:
            raise PermissionError("You can only edit your own ads")

        logger.info(f"Updating ad {ad.id} by user {user.username}")

        with transaction.atomic():
            for field, value in kwargs.items():
                if hasattr(ad, field):
                    setattr(ad, field, value)

            ad.full_clean()
            ad.save()

        logger.info(f"Ad {ad.id} updated successfully")
        return ad

    @staticmethod
    def delete_ad(ad: Ad, user: User) -> None:
        """ Удаление объявления """

        if ad.user != user:
            raise PermissionError("You can only delete your own ads")

        logger.info(f"Deleting ad {ad.id} by user {user.username}")

        with transaction.atomic():
            # Delete related exchange proposals first
            ExchangeProposal.objects.filter(
                Q(ad_sender=ad) | Q(ad_receiver=ad)
            ).delete()
            ad.delete()

        logger.info(f"Ad {ad.id} deleted successfully")

    @staticmethod
    def search_ads(query: Optional[str] = None,
                   category: Optional[str] = None,
                   condition: Optional[str] = None,
                   exclude_user: Optional[User] = None) -> QuerySet[Ad]:
        """ Поиск объявлений с фильтрами """

        queryset = Ad.objects.select_related('user').order_by('-created_at')

        if exclude_user:
            queryset = queryset.exclude(user=exclude_user)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset


class ExchangeProposalService:
    """Класс сервиса для бизнес-логики предложений обмена"""

    @staticmethod
    def create_proposal(sender_user: User, ad_sender: Ad, ad_receiver: Ad,
                        comment: str = '') -> ExchangeProposal:
        """ Создание нового предложения обмена """

        # Business logic validations
        if ad_sender.user != sender_user:
            raise ValidationError("You can only exchange your own ads")

        if ad_receiver.user == sender_user:
            raise ValidationError(
                "You cannot exchange with your own ads"
            )

        logger.info(
            f"Creating exchange proposal: {ad_sender.id} -> {ad_receiver.id}"
        )

        try:
            with transaction.atomic():
                proposal = ExchangeProposal(
                    ad_sender=ad_sender,
                    ad_receiver=ad_receiver,
                    comment=comment.strip()
                )
                proposal.full_clean()
                proposal.save()

            logger.info(f"Exchange proposal created with ID: {proposal.id}")
            return proposal

        except IntegrityError as e:
            logger.warning(
                f"Duplicate proposal attempt: "
                f"{ad_sender.id} -> {ad_receiver.id}"
            )
            # Check if it's a unique constraint violation
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                raise ValidationError(
                    "You have already sent a proposal for this ad"
                )
            else:
                raise ValidationError("Database integrity error occurred")

    @staticmethod
    def update_proposal_status(proposal: ExchangeProposal, user: User,
                               status: str) -> ExchangeProposal:
        """ Обновление статуса предложения обмена """

        if proposal.ad_receiver.user != user:
            raise PermissionError(
                "Only the receiver can update proposal status"
            )

        if status not in ['accepted', 'rejected']:
            raise ValidationError("Invalid status")

        logger.info(
            f"Updating proposal {proposal.id} status to {status} "
            f"by user {user.username}"
        )

        with transaction.atomic():
            proposal.status = status
            proposal.save()

            # If accepted, reject all other proposals for the same receiver ad
            if status == 'accepted':
                ExchangeProposal.objects.filter(
                    ad_receiver=proposal.ad_receiver,
                    status='pending'
                ).exclude(id=proposal.id).update(status='rejected')

        logger.info(f"Proposal {proposal.id} status updated to {status}")
        return proposal

    @staticmethod
    def get_user_proposals(
        user: User,
        filter_type: str = 'all',
        status: Optional[str] = None
    ) -> Tuple[QuerySet, QuerySet]:
        """ Получение предложений обмена пользователя """

        sent_base = ExchangeProposal.objects.filter(
            ad_sender__user=user
        ).select_related(
            'ad_sender', 'ad_receiver', 'ad_receiver__user'
        )

        received_base = ExchangeProposal.objects.filter(
            ad_receiver__user=user
        ).select_related(
            'ad_sender', 'ad_receiver', 'ad_sender__user'
        )

        # Apply status filter
        if status:
            sent_base = sent_base.filter(status=status)
            received_base = received_base.filter(status=status)

        # Apply type filter
        if filter_type == 'sent':
            return (sent_base.order_by('-created_at'),
                    ExchangeProposal.objects.none())
        elif filter_type == 'received':
            return (ExchangeProposal.objects.none(),
                    received_base.order_by('-created_at'))
        else:
            return (sent_base.order_by('-created_at'),
                    received_base.order_by('-created_at'))


class ValidationService:
    """Класс сервиса для валидации"""

    @staticmethod
    def validate_image_url(url: str) -> bool:
        """ Проверка URL изображения """

        if not url:
            return True  # Optional field

        from urllib.parse import urlparse

        import requests

        try:
            # Check URL format
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False

            # Check if URL responds and is an image
            response = requests.head(url, timeout=5)
            content_type = response.headers.get('content-type', '')

            return (response.status_code == 200 and
                    content_type.startswith('image/'))

        except Exception:
            return False

    @staticmethod
    def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
        """ Очистка и валидация текста """

        if not text:
            return ""

        sanitized = ' '.join(text.strip().split())

        if max_length and len(sanitized) > max_length:
            raise ValidationError(
                f"Text too long (max {max_length} characters)")

        return sanitized
