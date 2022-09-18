
import csv
import os
import django
from django.conf import settings
from reviews.models import Genre, Category, Title, Review, Comment, User

path = '/Users/yar/Dev/api_yamdb/api_yamdb/static/data'
os.chdir(path)


with open('users.csv') as file:
    data = csv.DictReader(file)
    for row in data:
        p = User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )
        p.save()

