from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, UserSignupViewSet,
    TokenViewSet, TitleViewSet,
    GenreViewSet, CategoryViewSet,
    ReviewViewSet, CommentViewSet
)

app_name = 'api'

# from api.views import 
router = SimpleRouter()

router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserSignupViewSet.as_view(), name='get_token'),
    path('auth/token/', TokenViewSet.as_view(), name='sign_up')
]

