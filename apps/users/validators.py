import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordValidator:
    """
    Кастомный валидатор пароля.
    Требует минимум одну цифру и минимум одну заглавную букву.
    """

    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                _('Пароль должен содержать минимум одну цифру.'),
                code='password_no_digit',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Пароль должен содержать минимум одну заглавную букву.'),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            'Пароль должен содержать минимум одну цифру '
            'и одну заглавную букву.'
        )
