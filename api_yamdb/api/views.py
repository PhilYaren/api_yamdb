from multiprocessing.spawn import import_main_path
from django.shortcuts import render
from django.db.models import Avg
from rest_framework import viewsets, views
from rest_framework.response import Response

from reviews.models import Category, Genre, Title
from .permissions import (
    AdminOnly, IsAdminOrReadOnly, IsModeratorAuthorOrReadOnly
)
from .serializers import (
    AdminSerializer, UserSerializer,
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TitlePostSerializer
)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    


    def get_serializer_class(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            serializer_class = AdminSerializer
        else:
            pass







class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))#.order_by('name')
    ordering = ['name']
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer



class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer   # Опечатка в имени сериализатора
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)



class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass

