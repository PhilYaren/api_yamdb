
import uuid
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Category, Genre, Title, User, Review
from .permissions import (
    AdminOnly, IsAdminOrReadOnly, IsModeratorAuthorOrReadOnly
)
from .filter import TitleFilter

from .serializers import (
    AdminSerializer, TokenSerializer, UserSerializer,
    SignUpSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer,
    TitlePostSerializer
)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    ordering = ['id']
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'username'
    permission_classes = (AdminOnly, IsAuthenticated)
    search_fields = ('username'),

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def get_your_info(self, request):
        serializer = UserSerializer(instance=request.user)
        if request.method == 'PATCH':
            if request.user.is_admin or request.user.is_superuser:
                serializer = AdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserSerializer(
                    instance=request.user,
                    data=request.data,
                    partial=True

                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data)


class UserSignupViewSet(views.APIView):
    def post(self, request):
        serializer = SignUpSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save(confirmation_code=uuid.uuid4())
        email_text = (
            f'''
            Добрый день, {user.username}!
            Спасибо что зарегистрировались в нашем приложении.
            Dаш код доступа - {user.confirmation_code}.
            '''
        )
        email = EmailMessage(
            to=[user.email],
            subject='Регистрация на YAMDB',
            body=email_text
        )
        email.send()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])

        if user.confirmation_code == serializer.data['confirmation_code']:
            access_token = str(AccessToken.for_user(user))
            return Response(
                data={'token': access_token},
                status=status.HTTP_200_OK)
        return Response(
            data={'token': 'Не верный токен'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    ordering = ['name']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer


class GenreViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        rewiews = title.reviews.all()
        return rewiews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
