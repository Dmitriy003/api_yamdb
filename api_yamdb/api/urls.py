from django.urls import include, path
from rest_framework import routers

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet, UserViewSet
from api.views import get_token, register

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='token'),
]
