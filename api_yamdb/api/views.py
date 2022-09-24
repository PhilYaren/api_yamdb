import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filter import TitleFilter
from .mixins import WorkingWithListViewSet
from .permissions import (
    AdminOnly, IsAdminOrReadOnly, IsModeratorAuthorOrReadOnly
)
from .serializers import (
    AdminSerializer, TokenSerializer, UserSerializer,
    SignUpSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer,
    TitlePostSerializer
)
from reviews.models import Category, Genre, Title, User, Review


SIGNUP_ERROR = '{value} уже занят. Используйте другой {field}.'


# class WorkingWithListViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet
# ):
#     pass


# class GenreCategoryViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet
#     ):
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = (SearchFilter,)
#     search_fields = ('name',)
#     lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    ordering = ['id']
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def get_your_info(self, request):
        serializer = UserSerializer(instance=request.user)
        if request.method == 'PATCH':
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
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get_or_create(
                username=username, email=email
            )[0]
            user.confirmattion_code = uuid.uuid4()
            user.save()
            email_text = (
                f'''
                Добрый день, {user.username}!
                Спасибо что зарегистрировались в нашем приложении.
                Ваш код доступа - {user.confirmation_code}.
                '''
            )
            email = EmailMessage(
                to=[user.email],
                subject='Регистрация на YAMDB',
                body=email_text,
                from_email=settings.MAIN_EMAIL
            )
            email.send()
        except IntegrityError:
            if User.objects.filter(username=username).exists():
                return Response(
                    SIGNUP_ERROR.format(value=username, field='username'),
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                SIGNUP_ERROR.format(value=email, field='email'),
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data.get('username'))
        if (
            user.confirmation_code
            == serializer.validated_data['confirmation_code']
        ):
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
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer


class GenreViewSet(WorkingWithListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(WorkingWithListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
