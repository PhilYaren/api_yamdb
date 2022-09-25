import re

from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class UsernameValidatorMixin:
    @classmethod
    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                message=f'Ник {value} запрещен'
            )
        check = ''.join(re.findall(r'[\w.@+-]+', value))
        if value != check:
            restricted_chars = ''.join(set(value) - set(check))
            raise ValidationError(
                message=f'В нике нельзя использовать {restricted_chars}'
            )
        return value


def current_year():
    return timezone.now().year


# Динамический валидатор с переопределением
# limit_value при каждом вызове
class DynamicMaxYearValidator(MaxValueValidator):
    def __call__(self, value):
        cleaned = self.clean(value)
        limit_value = self.limit_value()
        params = {
            'limit_value': limit_value,
            'show_value': cleaned,
            'value': value
        }
        if self.compare(cleaned, limit_value):
            raise ValidationError(self.message, code=self.code, params=params)
