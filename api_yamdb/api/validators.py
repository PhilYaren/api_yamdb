from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def no_me_username(value):
    if value == 'me':
        raise ValidationError(
            message=f'Имя пользователя {value} заблокированно'
        )
    
only_allowed_characters = RegexValidator(
    r'^[\w.@+-]+\z',
    message='Такие символы нельзя использовать в никнейме'
)