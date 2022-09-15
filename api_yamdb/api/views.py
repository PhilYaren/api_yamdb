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
    GenreSeializer, ReviewSerializer,
    TitleSerializer
)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    


    def get_serializer_class(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            serializer_class = AdminSerializer
        else:
            pass







class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all() # рейтинг Avg? через .annotate?
    permission_classes = (IsAdminOrReadOnly,)



class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSeializer   # Опечатка в имени сериализатора

    def get_serializer_class(self):
        pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass

