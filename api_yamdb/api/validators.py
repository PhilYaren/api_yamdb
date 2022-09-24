import re

from rest_framework.validators import ValidationError


class UsernameValidatorMixin:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                detail={
                    'username': 'Ник me нельзя выбрать'
                }
            )

        if value != re.search(r'^[-a-zA-Z0-9_@.+]+', value).group():
            raise ValidationError(
                detail={
                    'username': 'Такие символы нельзя использовать в никнейме'
                }
            )
        return value
