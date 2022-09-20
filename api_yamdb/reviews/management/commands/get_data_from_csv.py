import csv

from django.core.management.base import BaseCommand
from api_yamdb.settings import STATICFILES_DIRS
from reviews.models import Category, Comment, Genre, Review, Title, User


SIMPLE_MODELS = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Выгрузка моделей без сторонних связей
        for model, csv_name in SIMPLE_MODELS.items():
            with open(
                file=f'{STATICFILES_DIRS[0]}data/{csv_name}',
                mode='r', encoding='utf-8'
            ) as csv_file:
                file = csv.DictReader(csv_file)

                for row in file:
                    model(**row).save()
                self.stdout.write(msg=f'Файлы из {csv_name} выгружены в базу')

        # Выгрузка Titles
        with open(
            file=f'{STATICFILES_DIRS[0]}data/titles.csv',
            mode='r', encoding='utf-8', newline=''
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'], name=row['name'], year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
            self.stdout.write(msg='Файлы из titles.csv выгружены в базу')

        # Выгрузка Обзоров
        with open(
            file=f'{STATICFILES_DIRS[0]}data/review.csv',
            mode='r', encoding='utf-8', newline=''
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'], title=Title.objects.get(id=row['title_id']),
                    text=row['text'], author=User.objects.get(
                        id=row['author']),
                    score=row['score'], pub_date=row['pub_date']
                )
            self.stdout.write(msg='Файлы из review.csv выгружены в базу')

        # Выгрузка Комментариев
        with open(
            file=f'{STATICFILES_DIRS[0]}data/comments.csv',
            mode='r', encoding='utf-8', newline=''
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Comment.objects.get_or_create(
                    id=row['id'], review=Review.objects.get(
                        id=row['review_id']),
                    text=row['text'], author=User.objects.get(
                        id=row['author']),
                    pub_date=row['pub_date']
                )
            self.stdout.write(msg='Файлы из comments.csv выгружены в базу')

        # Выгрузка связей Жанров и произведений
        with open(
            file=f'{STATICFILES_DIRS[0]}data/genre_title.csv',
            mode='r', encoding='utf-8', newline=''
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Genre.objects.get(
                    id=row['genre_id']).titles.add(
                        Title.objects.get(id=row['title_id']))
            self.stdout.write(msg='Файлы из genre_title.csv выгружены в базу')

        self.stdout.write(msg='Выгрузка данных завершена')
