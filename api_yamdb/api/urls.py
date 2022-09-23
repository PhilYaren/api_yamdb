from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, UserSignupViewSet,
    TokenViewSet, TitleViewSet,
    GenreViewSet, CategoryViewSet,
    ReviewViewSet, CommentViewSet
)

app_name = 'api'
router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', UserSignupViewSet.as_view(), name='get_token'),
    path('token/', TokenViewSet.as_view(), name='sign_up')
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_patterns))
]
