from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api_yamdb.settings import (
    USER_NAMES_LENGTH, USER_EMAIL_LENGTH,
    USER_CONFIRM_CODE_LENGTH, CATEGORYGENRE_NAME_LENGTH,
    CATEGORYGENRE_SLUG_LENGTH, TITLE_NAME_LENGTH,
    TITLE_DESCRIPTION_LENGTH
)
from .validators import OnlyAllowedCharacters, no_me_username
from .utils import ADMIN, MODERATOR, USER

# Прописаны роли для пользователей
USER_ROLES = (
    (ADMIN, ADMIN),
    (USER, USER),
    (MODERATOR, MODERATOR)
)


class User(AbstractUser):
    '''Переопределение полей пользователя'''
    username = models.CharField(
        max_length=USER_NAMES_LENGTH,
        verbose_name='Юзернейм',
        validators=(
            no_me_username,  # Запрет на имя me
            OnlyAllowedCharacters  # Запрет на определенные символы
        ),
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        max_length=USER_NAMES_LENGTH,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=USER_NAMES_LENGTH,
        verbose_name='Фамилия',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=USER_EMAIL_LENGTH,
        blank=False,
        unique=True
    )
    role = models.CharField(
        verbose_name='Уровень доступа',
        max_length=max([len(role) for role, _ in USER_ROLES]),
        choices=USER_ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=USER_CONFIRM_CODE_LENGTH,
        null=True
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self) -> str:
        return self.username[:50]


class CategoryGenre(models.Model):
    '''Абстрактная модель жанров и категорий'''
    name = models.CharField(max_length=CATEGORYGENRE_NAME_LENGTH)
    slug = models.SlugField(max_length=CATEGORYGENRE_SLUG_LENGTH, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Category(CategoryGenre):
    """Модель категории"""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(CategoryGenre):
    """Модель жанры"""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=TITLE_NAME_LENGTH,
        db_index=True
    )
    year = models.SmallIntegerField(
        verbose_name='год',
        validators=(
            MaxValueValidator(
                timezone.now().year,
                message='Не возможно добавить еще не вышедшие произведения'
            ),
        ),
        db_index=True
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
        max_length=TITLE_DESCRIPTION_LENGTH,
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


class ReviewComment(models.Model):
    text = models.TextField(
        verbose_name='Обзор'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        abstract = True
        default_related_name = '%(class)ss'


class Review(ReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        default=5,
        validators=(
            MinValueValidator(
                limit_value=1,
                message='Рейтинг не может быть менее 1'
            ),
            MaxValueValidator(
                limit_value=10,
                message='Рейтинг не может быть более 10'
            )
        )
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='Только одно ревью от пользователя на одно произведение'
            ),
        )


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
