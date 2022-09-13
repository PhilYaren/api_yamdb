from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import MaxValueValidator
from django.utils import timezone
from api.validators import only_allowed_characters, no_me_username
# Create your models here.


# Прописаны роли для пользователей
USER_ROLES = [
    ('admin', 'admin'),
    ('user', 'user'),
    ('moderator', 'moderator')
]


# Нужно доделать
class User(AbstractUser):
    '''Переопределение полей пользователя'''
    username = models.CharField(
        max_length=150,
        validators=(
            no_me_username, # Запрет на имя me
            only_allowed_characters # Запрет на определенные символы
        ),
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        unique=True,
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    email =  models.EmailField(
        max_length=254,
        blank=False
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(
        blank=True
    )



class Category(models.Model):
    '''Категории произведений'''
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        blank=False,
        unique=True,
    )


class Genres(models.Model):
    '''Жанры произведений'''
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        blank=False,
        unique=True
    )


class Titles(models.Model):
    '''Произведения'''
    name = models.CharField(
        max_length=256
    )
    year = models.IntegerField(
        validators=(MaxValueValidator(timezone.now().year),) # Валидатор на проверку года. Если год больше текущего - вернет ошибку
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL
    )

# Можно и не делать такую таблицу(Ввести ManyToManyField в Titles), но тут проще будет прописать UniqueConstraints
class GenreTitle(models.Model):
    '''Модель связи жанров и произведений'''
    title = models.ForeignKey(
        Titles,
        related_name='titles_with_genre',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genres, 
        related_name='genres_of_title',
        on_delete= models.CASCADE
    )


class Review(models.Model):
    pass


class Comments(models.Model):
    pass
