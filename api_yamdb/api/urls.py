from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, UserSignupViewSet,
    TokenViewSet, TitleViewset,
    GenreViewset, CategoryViewSet,
    ReviewViewSet, CommentViewSet
)


app_name = 'api'

# from api.views import 
router = SimpleRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserSignupViewSet.as_view(), name='get_token'),
    path('auth/token/', TokenViewSet.as_view(), name='sign_up')
]