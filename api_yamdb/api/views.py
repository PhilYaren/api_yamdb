from multiprocessing.spawn import import_main_path
from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response

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

