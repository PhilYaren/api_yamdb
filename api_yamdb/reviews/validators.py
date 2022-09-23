from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def no_me_username(value):
    if value == 'me':
        raise ValidationError(
            message=f'Имя пользователя {value} заблокированно'
        )


class OnlyAllowedCharacters(RegexValidator):
    regex = r'^[\w.@+-]+\z'
    message = 'Такие символы нельзя использовать в никнейме'
    code = 'invalid_username'
