# Используемый стек
<p>
  <a 
  target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-_3.7-green.svg">
  </a>
  <a 
  target="_blank" href="https://www.djangoproject.com/download/" title="Django Framework"><img src="https://img.shields.io/badge/django-2.2-orange">
  </a>
  <a 
  target="_blank" href="https://www.django-rest-framework.org/" title="Django REST Framework"><img src="https://img.shields.io/badge/DRF-3.12-blue">
  </a>
  <a 
  target="_blank" href="https://django-filter.readthedocs.io/en/stable/" title="Django-filter"><img src="https://img.shields.io/badge/django--filter-21.1-brightgreen">
  </a>
  <a 
  target="_blank" href="https://django-rest-framework-simplejwt.readthedocs.io/en/latest/" title="JWT"><img src="https://img.shields.io/badge/DRF--SimpleJWT-5.0-red">
  </a>
</p>

# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

## Установка проекта и зависимостей локально:
Клонируйте проект себе на локальную машину:
```zsh
git clone git@github.com:PhilYaren/api_yamdb.git
```
Установите виртуальное окружение:
```zsh
python3 -m venv venv
```

Активируйте виртуальное окружение:
```zsh
source venv/bin/activate
```
Обновление pip:

```zsh
python -m pip install --upgrade pip
```

Установите необходимые зависимости:
```zsh
pip3 install -r "requirements.txt"
```

Для перехода к файлу manage.py введите:
```zsh
cd api_yamdb
```
(Опционально) есть возможность выгрузки тестовых данных с помощью скрипта:
```zsh
python3 manage.py get_data_from_csv
```

Для запуска проекта на локальной машине введите:
```zsh
python3 manage.py runserver
```

YaMDb будет доступен по адресу:
```zsh
http://127.0.0.1:8000
```

## Пользовательские роли
1. Аноним — может просматривать описания произведений, читать отзывы и комментарии.
2. Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
3. Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
4. Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Регистрация на проекте, а также получение токена:
Создание нового пользователя:
```zsh
POST /api/v1/auth/signup/
```
```json
{
  "email": "string",
  "username": "string"
}
```
После создания профиля, вам на почту придет письмо с кодом для авторизации (confirmation_code)
<br>
<br>
Получение access токена:
```
POST /api/v1/auth/token/
```
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

## Эндпоинты:
>```url
>GET /api/v1/categories/ - Категории (Книги, Музыка, Фильмы)
>GET /api/v1/genres/ - Жанры
>GET /api/v1/titles/ - Произведения
>GET /api/v1/titles/{title_id}/reviews/ - Отзывы к произведению
>GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Комментарии к отзыву
>GET /api/v1/users/me - Подробная информация о вашем аккаунте
>Доступно только Администраторам:
>GET /api/v1/users/ - Пользователи
>```


## Документация:
Подробная информация по эндпоинтам и доступным для них методам доступна на:
```zsh
http://127.0.0.1:8000/redoc/
```

Команда разработки:
#### [Ярослав Филиппов](https://github.com/PhilYaren)
#### [Юлия Суркова](https://github.com/Juliosity)
#### [Александр Чёрный](https://github.com/chyornyy)
