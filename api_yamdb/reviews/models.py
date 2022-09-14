from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import only_allowed_characters, no_me_username

"""От Саши: Описал модели по ТЗ"""
"""Не очень понял, что с Юзером делать"""
"""И еще не понял, что делать с ЖанрТитулом и зачем он"""

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
            no_me_username,  # Запрет на имя me
            only_allowed_characters  # Запрет на определенные символы
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
    email = models.EmailField(
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
    """Модель категории"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.slug


class Genre(models.Model):
    """Модель жанры"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'Год'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'ата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
